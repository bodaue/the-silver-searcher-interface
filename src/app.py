import gettext
import os
import subprocess
import threading
from pathlib import Path
from tkinter import filedialog
from tkinter.constants import NORMAL, DISABLED, END

import customtkinter

from src.ag_parser import AgParser
from src.config import *

customtkinter.set_default_color_theme(DEFAULT_COLOR_THEME)  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self, default_lang=DEFAULT_LANGUAGE):
        super().__init__()

        self.localedir = Path(__file__).parent
        self.localedir = os.path.join(self.localedir, '../locales')
        self.language = default_lang

        # configure window
        self.title(TITLE)
        self.geometry(f"{850}x{491}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text=TITLE,
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.entry_pattern = customtkinter.CTkEntry(master=self.sidebar_frame)
        self.entry_pattern.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create checkboxes (flags)
        self.checkbox_i = customtkinter.CTkCheckBox(master=self.sidebar_frame)
        self.checkbox_i.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="NSEW")
        self.checkbox_w = customtkinter.CTkCheckBox(master=self.sidebar_frame)
        self.checkbox_w.grid(row=3, column=0, pady=(20, 0), padx=20, sticky="NSEW")

        self.checkbox_c = customtkinter.CTkCheckBox(master=self.sidebar_frame)
        self.checkbox_c.grid(row=4, column=0, pady=(20, 0), padx=20, sticky="n")

        # create sidebar button
        self.main_button = customtkinter.CTkButton(self.sidebar_frame,
                                                   command=self.threading_apply_button_event,
                                                   width=200)
        self.main_button.grid(row=4, column=0, padx=20, pady=60, sticky='n')

        self.language_menu_label = customtkinter.CTkLabel(self.sidebar_frame, anchor='w')
        self.language_menu_label.grid(row=5, column=0, padx=20, pady=(0, 100), sticky='n')

        self.language_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                         values=["Русский", "English"],
                                                         command=self.set_language)
        self.language_menu.grid(row=5, column=0, padx=20, pady=(10, 50))

        # create appearance menu to change .env.dist theme
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(20, 0))
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=5, column=0, padx=20, pady=(80, 0))

        # choosing folder path
        self.entry_folder_path = customtkinter.CTkEntry(self)
        self.entry_folder_path.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.folder_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"),
                                                     command=self.filedialog_event,
                                                     text='...', width=50)
        self.folder_button.grid(row=3, column=3, padx=(10, 20), pady=(20, 20), sticky="nsew")

        self.textbox = customtkinter.CTkTextbox(self, width=250, height=400)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # set default values
        self.textbox.configure(state=DISABLED)
        self.appearance_mode_menu.set(DEFAULT_APPEARANCE_MODE)

        self.set_language(default_lang)

    def set_language(self, lang: str):
        self.language = 'ru' if lang in ('Русский', 'ru') else 'en'

        _ = gettext.translation('messages', localedir=self.localedir, languages=[self.language]).gettext

        # set texts
        self.entry_pattern.configure(placeholder_text=_("Паттерн"))
        self.checkbox_i.configure(text=_('Игнорировать регистр'))
        self.checkbox_w.configure(text=_('Поиск слов целиком'))
        self.checkbox_c.configure(text=_('Поиск количества вхождений'))
        self.main_button.configure(text=_('Применить'))
        self.language_menu_label.configure(text=_('Язык'))
        self.appearance_mode_label.configure(text=_('Цветовая тема'))
        self.entry_folder_path.configure(placeholder_text=_('Путь к каталогу'))

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def filedialog_event(self):
        filename = filedialog.askdirectory()
        self.entry_folder_path.delete(0, END)
        self.entry_folder_path.insert(index=0, string=filename)

    def apply_button_event(self):
        flag_i = '-i' if self.checkbox_i.get() else '-s'
        flag_w = '-w' if self.checkbox_w.get() else ''
        flag_c = '-c' if self.checkbox_c.get() else ''

        flags = f'{flag_i} {flag_w} {flag_c}'.strip()

        _ = gettext.translation('messages', localedir=self.localedir, languages=[self.language]).gettext

        pattern = self.entry_pattern.get()
        if not pattern:
            self._text_message(_('Введите паттерн!'))
            return

        folder = self.entry_folder_path.get()
        if not folder:
            self._text_message(_('Выберите каталог'))
            return

        self.main_button.configure(state=DISABLED)

        command_string = f'ag.exe -H --ackmate {flags} {pattern} {folder}'
        print(command_string)
        try:
            result = subprocess.run(command_string, capture_output=True, timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            self._text_message(_('Превышено время ожидания {} секунд.').format(TIMEOUT))
            self.main_button.configure(state=NORMAL)
            return

        self.main_button.configure(state=NORMAL)
        if result.stderr:
            self._text_message(result.stderr)
        else:
            result = result.stdout.decode('cp866')
            result = AgParser(result_string=result).format_text(flag_c=bool(self.checkbox_c.get()))
            result = result[:20000]
            self._text_message(result)

    def threading_apply_button_event(self):
        threading.Thread(target=self.apply_button_event).start()

    def _text_message(self, text):
        self.textbox.configure(state=NORMAL)
        self.textbox.delete(1.0, END)
        self.textbox.insert('0.0', text)
        self.textbox.configure(state=DISABLED)
