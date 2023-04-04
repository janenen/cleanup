from configparser import ConfigParser
import tkinter as tk
from tkinter import ttk
from idlelib.tooltip import Hovertip
from data.shooter import Shooter


class UserSettingsFrame(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        # field options
        options = {"padx": 5, "pady": 0}

        # constant labels
        ttk.Label(self, text="Name:").grid(column=0, row=0, sticky="e", **options)
        ttk.Label(self, text="Verein:").grid(column=0, row=1, sticky="e", **options)
        ttk.Label(self, text="Mannschaft:").grid(column=0, row=2, sticky="e", **options)

        self.name = tk.StringVar()
        self.name_entry = ttk.Entry(self, textvariable=self.name)
        self.name_entry.grid(column=1, row=0, sticky="w", **options)
        Hovertip(self.name_entry, "Name des Schützen")

        self.club = tk.StringVar()
        self.club_entry = ttk.Entry(self, textvariable=self.club)
        self.club_entry.grid(column=1, row=1, sticky="w", **options)
        Hovertip(self.club_entry, "Verein des Schützen")

        self.team = tk.StringVar()
        self.team_entry = ttk.Entry(self, textvariable=self.team)
        self.team_entry.grid(column=1, row=2, sticky="w", **options)
        Hovertip(self.team_entry, "Mannschaft des Schützen")

        self.save = tk.BooleanVar()
        self.save_box = tk.Checkbutton(self)
        self.save_box["text"] = "Speichern"
        self.save_box["variable"] = self.save
        self.save_box.grid(column=1, row=3, sticky="w", **options)
        Hovertip(self.save_box, "Daten des Schützen und Einstellungen speichern")

        # add padding to the frame and show it
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def reset(self, back=False):
        self.parent.back_button["state"] = "normal"
        self.parent.ok_button["state"] = "normal"

    def parseInput(self):
        name = self.name.get()
        club = self.club.get()
        team = self.team.get()
        new_shooter = Shooter(name=name, club=club, team=team)
        self.parent.competition.add_match(new_shooter)
        if self.save.get():
            self.save_shooter(name, club, team)
        return True

    def save_shooter(self, name, club, team):
        userconfig = ConfigParser()
        userconfigpath = "./schuetzen.ini"
        userconfig.read(userconfigpath)
        section_name = self.name.get().replace(" ", "")
        userconfig[section_name] = {
            "Name": name,
            "Verein": club,
            "Mannschaft": team,
            "niceness": 0,
        }
        with open(userconfigpath, "w") as configfile:
            userconfig.write(configfile)
