import tkinter as tk
import sys
import os

from ui.frames.control_frame import ControlFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Auswertung")
        self.geometry("800x320")
        self.resizable(True, True)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)


if __name__ == "__main__":
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    app = App()
    app.iconbitmap(os.path.join(base_path, "ui", "logo.ico"))
    try:
        import pyi_splash

        pyi_splash.close()
    except Exception:
        pass
    ControlFrame(app)
    app.mainloop()
