import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from datetime import date
from idlelib.tooltip import Hovertip
from data.club import Club
from data.league import RSBLeague
from data.match import RADIUS_DICT
from data.competition import Competition, SORTING_FUNCTION
from data.team import Team
from .default_frame import DefaultFrame

LEAGUES = ["Kreisliga", "Bezirksliga", "Landesliga"]


class RSBLeagueFrame(DefaultFrame):
    def __init__(self, container, parent):
        super().__init__(container, parent)
        # field options
        options = {"padx": 5, "pady": 0}

        # constant labels
        ttk.Label(self, text="Disziplin:").grid(column=0, row=0, sticky="e", **options)
        ttk.Label(self, text="Liga:").grid(column=0, row=1, sticky="e", **options)
        ttk.Label(self, text="Gruppe:").grid(column=0, row=2, sticky="e", **options)
        ttk.Label(self, text="Heimverein:").grid(column=0, row=3, sticky="e", **options)
        ttk.Label(self, text="Heimmannschaft:").grid(
            column=0, row=4, sticky="e", **options
        )
        ttk.Label(self, text="Gastverein:").grid(column=0, row=5, sticky="e", **options)

        ttk.Label(self, text="Gastmannschaft:").grid(
            column=0, row=6, sticky="e", **options
        )

        self.discipline = tk.StringVar()
        self.discipline_entry = ttk.Entry(self, textvariable=self.discipline)
        self.discipline_entry.grid(column=1, row=0, sticky="w", **options)
        Hovertip(
            self.discipline_entry,
            "Disziplin",
        )
        self.league_name = tk.StringVar()
        self.league_menu = tk.OptionMenu(self, self.league_name, *LEAGUES)

        self.league_menu.grid(column=1, row=1, sticky="w", **options)
        Hovertip(
            self.league_menu,
            "Liga",
        )

        self.group = tk.StringVar()
        self.group_entry = ttk.Entry(self, textvariable=self.group)
        self.group_entry.grid(column=1, row=2, sticky="w", **options)
        Hovertip(self.group_entry, "Gruppe")

        self.home_club = ttk.Label(self, text="Verein Auswählen")
        self.home_club.grid(column=1, row=3, sticky="w", **options)

        self.home_team = ttk.Label(self, text="Mannschaft Auswählen")
        self.home_team.grid(column=1, row=4, sticky="w", **options)

        self.guest_club = ttk.Label(self, text="Verein Auswählen")
        self.guest_club.grid(column=1, row=5, sticky="w", **options)

        self.guest_team = ttk.Label(self, text="Mannschaft Auswählen")
        self.guest_team.grid(column=1, row=6, sticky="w", **options)

        self.home_club_button = ttk.Button(self, text="Auswählen")
        self.home_club_button.grid(column=3, row=3, sticky="w", **options)
        Hovertip(self.home_club_button, "Heimverein auswählen")
        self.home_club_button.configure(command=self.select_home_club)

        self.home_team_button = ttk.Button(self, text="Auswählen")
        self.home_team_button.grid(column=3, row=4, sticky="w", **options)
        Hovertip(self.home_team_button, "Heimmannschaft auswählen")
        self.home_team_button.configure(command=self.select_home_team)

        self.guest_club_button = ttk.Button(self, text="Auswählen")
        self.guest_club_button.grid(column=3, row=5, sticky="w", **options)
        Hovertip(self.guest_club_button, "Gastverein auswählen")
        self.guest_club_button.configure(command=self.select_guest_club)

        self.guest_button = ttk.Button(self, text="Auswählen")
        self.guest_button.grid(column=3, row=6, sticky="w", **options)
        Hovertip(self.guest_button, "Gastmannschaft auswählen")
        self.guest_button.configure(command=self.select_guest_team)

        # add padding to the frame and show it
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
        self.select_home_club_var = False
        self.select_home_team_var = False
        self.select_guest_club_var = False
        self.select_guest_team_var = False
        self.club_home = None
        self.team_home = None
        self.club_guest = None
        self.team_guest = None

    def home_club_to_select(self):
        return self.select_home_club_var

    def select_home_club(self):
        self.select_home_club_var = True
        self.proceed()

    def home_team_to_select(self):
        return self.select_home_team_var

    def select_home_team(self):
        self.select_home_team_var = True
        self.proceed()

    def guest_club_to_select(self):
        return self.select_guest_club_var

    def select_guest_club(self):
        self.select_guest_club_var = True
        self.proceed()

    def guest_team_to_select(self):
        return self.select_guest_team_var

    def select_guest_team(self):
        self.select_guest_team_var = True
        self.proceed()

    def reset(self):
        if self.club_home:
            self.home_club.config(text=self.clubs[self.club_home].name)
        if self.team_home:
            self.home_team.config(text=self.teams[self.team_home].name)
        if self.club_guest:
            self.guest_club.config(text=self.clubs[self.club_guest].name)
        if self.team_guest:
            self.guest_team.config(text=self.teams[self.team_guest].name)

        self.activate_back_button()
        self.activate_ok_button()

    def parseInput(self):
        if not (
            self.club_home and self.team_home and self.club_guest and self.team_guest
        ):
            return False
        self.league = RSBLeague(
            discipline=self.discipline.get(),
            league=self.league_name.get(),
            group=self.group.get(),
            home_club=self.club_home,
            home_team=self.team_home,
            guest_club=self.club_guest,
            guest_team=self.team_guest,
        )
        self.competition.league = self.leagues.add_league(self.league)
        self.leagues.save()
        self.competitions.save()
        return True
