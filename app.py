import subprocess
from pathlib import Path
from tkinter import filedialog
from tkinter.constants import NORMAL, DISABLED, END

import customtkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"

customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.folder_path = Path()

        # configure window
        self.title("The Silver Searcher")
        self.geometry(f"{850}x{450}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="The Silver Searcher",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.entry_pattern = customtkinter.CTkEntry(master=self.sidebar_frame,
                                                    placeholder_text="Паттерн")
        self.entry_pattern.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create checkboxes
        self.checkbox_i = customtkinter.CTkCheckBox(master=self.sidebar_frame,
                                                    text='Игнорировать регистр')
        self.checkbox_i.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="NSEW")
        self.checkbox_w = customtkinter.CTkCheckBox(master=self.sidebar_frame,
                                                    text='Поиск слов целиком')
        self.checkbox_w.grid(row=3, column=0, pady=(20, 0), padx=20, sticky="NSEW")

        self.checkbox_c = customtkinter.CTkCheckBox(master=self.sidebar_frame,
                                                    text='Поиск количества вхождений')
        self.checkbox_c.grid(row=4, column=0, pady=(20, 0), padx=20, sticky="n")
        # create sidebar button
        self.main_button = customtkinter.CTkButton(self.sidebar_frame,
                                                   command=self.apply_button_event,
                                                   text='Применить',
                                                   width=200)
        self.main_button.grid(row=4, column=0, padx=20, pady=60, sticky='n')

        # create appearance menu to change a theme
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # create main entry and button
        self.entry_folder_path = customtkinter.CTkEntry(self, placeholder_text="Путь к каталогу")
        self.entry_folder_path.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.folder_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"),
                                                     command=self.filedialog_event,
                                                     text='...', width=50)
        self.folder_button.grid(row=3, column=3, padx=(10, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250, height=400)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # set default values
        self.textbox.configure(state=DISABLED)
        self.appearance_mode_menu.set("Dark")

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def filedialog_event(self):
        filename = filedialog.askdirectory()
        self.folder_path = filename
        self.entry_folder_path.insert(index=0, string=filename)

    def apply_button_event(self):
        flag_i = '-i' if self.checkbox_i.get() else ''
        flag_w = '-w' if self.checkbox_w.get() else ''
        flag_c = '-c' if self.checkbox_c.get() else ''

        flags = f'{flag_i} {flag_w} {flag_c}'.strip()

        pattern = self.entry_pattern.get()
        if not pattern:
            self.text_message('Введите паттерн!')
            return

        folder = self.entry_folder_path.get()
        if not folder:
            self.text_message('Выберите каталог!')
            return

        command_string = f'ag {flags} {pattern} {folder}'
        result = subprocess.run(command_string, capture_output=True)
        if result.stderr:
            self.text_message(result.stderr)
        else:
            self.text_message(result.stdout.decode('cp866'))

    def text_message(self, text):
        self.textbox.configure(state=NORMAL)
        self.textbox.delete(1.0, END)
        self.textbox.insert('0.0', text)
        self.textbox.configure(state=DISABLED)


if __name__ == "__main__":
    app = App()
    app.mainloop()
