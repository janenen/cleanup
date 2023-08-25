import tkinter as tk
from tkinter import ttk
from idlelib.tooltip import Hovertip
from data.team import Team
from .default_frame import DefaultFrame


class TeamSettingsFrame(DefaultFrame):
    def __init__(self, container, parent):
        super().__init__(container, parent)
        # field options
        options = {"padx": 5, "pady": 0}
        # constant labels
        ttk.Label(self, text="Name:").grid(column=0, row=0, sticky="e", **options)

        self.name = tk.StringVar()
        self.name_entry = ttk.Entry(self, textvariable=self.name)
        self.name_entry.grid(column=1, row=0, sticky="w", **options)
        Hovertip(self.name_entry, "Name der Mannschaft")

        self.save = tk.BooleanVar()
        self.save_box = tk.Checkbutton(self)
        self.save_box["text"] = "Speichern"
        self.save_box["variable"] = self.save
        self.save_box.grid(column=1, row=3, sticky="w", **options)
        Hovertip(self.save_box, "Daten des Schützen und Einstellungen speichern")

        # add padding to the frame and show it
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

    def reset(self):
        self.name.set("")
        if self.team:  # user selected to edit
            self.name.set(self.team.name)
        self.activate_back_button()
        self.activate_ok_button()

    def parseInput(self):
        name = self.name.get()
        if name == "":
            return
        self.team = Team(name)
        if self.save.get():
            self.teams.add_team(self.team)
            self.teams.save()
        return True
