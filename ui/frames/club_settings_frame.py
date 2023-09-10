import tkinter as tk
from tkinter import ttk
from idlelib.tooltip import Hovertip
from data.club import Club
from .default_frame import DefaultFrame


class ClubSettingsFrame(DefaultFrame):
    def __init__(self, container, parent):
        super().__init__(container, parent)
        options = {"padx": 5, "pady": 0}
        # constant labels
        ttk.Label(self, text="Name:").grid(column=0, row=0, sticky="e", **options)

        self.name = tk.StringVar()
        self.name_entry = ttk.Entry(self, textvariable=self.name)
        self.name_entry.grid(column=1, row=0, sticky="w", **options)
        Hovertip(self.name_entry, "Name des Vereins")

        self.save = tk.BooleanVar()
        self.save_box = tk.Checkbutton(self)
        self.save_box["text"] = "Speichern"
        self.save_box["variable"] = self.save
        self.save_box.grid(column=1, row=3, sticky="w", **options)
        Hovertip(self.save_box, "Daten des Vereins speichern")

        # add padding to the frame and show it
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

    def reset(self):
        self.name.set("")
        if self.club:  # club selected to edit
            self.name.set(self.club.name)
        self.save.set(False)
        self.activate_back_button()
        self.activate_ok_button()

    def parseInput(self):
        name = self.name.get()
        if name == "":
            return
        if self.club:
            self.club.name = name
        else:
            self.club = Club(name)
            if self.save.get():
                self.clubs.add_club(self.club)
        if self.save.get():
            self.clubs.save()
        return True
