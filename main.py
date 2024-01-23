from src.app import App
from src.config import DEFAULT_LANGUAGE

if __name__ == "__main__":
    app = App(default_lang=DEFAULT_LANGUAGE)
    app.mainloop()
