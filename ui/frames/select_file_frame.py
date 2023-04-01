import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from idlelib.tooltip import Hovertip
from machines.csv import CSV
from machines.qsd import QSD


class SelectFileFrame(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        self.container = container
        # field options
        options = {"padx": 5, "pady": 0}
        self.test_label = ttk.Label(self, text="")
        self.test_label.grid(column=0, row=0, sticky="nesw", **options)
        self.start_button = tk.Button(self, text="Datei auswählen", command=self.reset)
        Hovertip(self.start_button, "Datei zum Einlesen auswählen")
        self.start_button.grid(column=0, row=1, sticky="e", **options)

        # add padding to the frame and show it
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def reset(self, back=False):
        self.container.withdraw()
        if self.parent.usersection == "Neu":
            filepath = "./"
        else:
            filepath = self.parent.match.name.replace(" ", "_")
        if type(self.parent.quelle) == CSV:
            filetype = ("CSV Dateien", "*.csv")
        elif type(self.parent.quelle) == QSD:
            filetype = ("QuickShot Dateien", "*.qsd")
        self.parent.inputfile = filedialog.askopenfilename(
            initialdir=filepath,
            filetypes=[filetype],
        )
        self.container.deiconify()
        if os.path.isfile(self.parent.inputfile):
            self.parent.ok_button["state"] = "normal"
        else:
            self.parent.ok_button["state"] = "disabled"
        self.test_label.config(text=self.parent.inputfile)
