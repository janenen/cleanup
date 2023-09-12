import tkinter as tk
from tkinter import ttk
from idlelib.tooltip import Hovertip
from .default_frame import DefaultFrame

querry_list = ["Mannschaft", "Match", "Schütze", "Verein", "Wettbewerb"]


class DatabaseBrowserFrame(DefaultFrame):
    def __init__(self, container, parent):
        super().__init__(container, parent)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=0)
        ttk.Label(self, text="Suche:").grid(column=0, row=0, sticky="e")
        self.desired_querry = tk.StringVar()
        self.desired_querry_menu = tk.OptionMenu(
            self, self.desired_querry, *querry_list, command=self.querry
        )
        self.desired_querry_menu.grid(column=1, row=0, sticky="w")
        Hovertip(
            self.desired_querry_menu,
            "Wonach soll gesucht werden?",
        )

        ttk.Label(self, text="Mannschaft:").grid(column=2, row=0, sticky="e")
        self.team_selected = tk.StringVar()
        self.team_selected_menu = tk.OptionMenu(
            self, self.team_selected, *[team[1].name for team in self.teams], command=self.by_team
        )
        self.team_selected_menu.grid(column=3, row=0, sticky="w")
        Hovertip(
            self.team_selected_menu,
            "Mannschaft auswählen",
        )

        ttk.Label(self, text="Match:").grid(column=2, row=1, sticky="e")
        self.match_selected = tk.StringVar()
        self.match_selected_menu = tk.OptionMenu(
            self, self.match_selected, *[match[1].date for match in self.matches]
        )
        self.match_selected_menu.grid(column=3, row=1, sticky="w")
        Hovertip(
            self.match_selected_menu,
            "Match auswählen",
        )

        ttk.Label(self, text="Schütze:").grid(column=2, row=2, sticky="e")
        self.user_selected = tk.StringVar()
        self.user_selected_menu = tk.OptionMenu(
            self, self.user_selected, *[user[1].name for user in self.users]
        )
        self.user_selected_menu.grid(column=3, row=2, sticky="w")
        Hovertip(
            self.user_selected_menu,
            "Schütze auswählen",
        )

        ttk.Label(self, text="Verein:").grid(column=2, row=3, sticky="e")
        self.club_selected = tk.StringVar()
        self.club_selected_menu = tk.OptionMenu(
            self, self.club_selected, *[club[1].name for club in self.clubs]
        )
        self.club_selected_menu.grid(column=3, row=3, sticky="w")
        Hovertip(
            self.club_selected_menu,
            "Verein auswählen",
        )

        ttk.Label(self, text="Wettkampf:").grid(column=2, row=4, sticky="e")
        self.competition_selected = tk.StringVar()
        self.competition_selected_menu = tk.OptionMenu(
            self,
            self.competition_selected,
            *[competition[1].name for competition in self.competitions]
        )
        self.competition_selected_menu.grid(column=3, row=4, sticky="w")
        Hovertip(
            self.competition_selected_menu,
            "Wettbewerb auswählen",
        )
        self.scrollbar = tk.Scrollbar(self)
        self.querrylistbox = tk.Listbox(self, height=5, width=50)

        # self.querrylistbox.bind("<<ListboxSelect>>", self.select)
        self.querrylistbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.querrylistbox.yview)
        self.scrollbar.grid(column=5, row=5, sticky="wens")
        self.querrylistbox.grid(columnspan=5, column=0, row=5, sticky="ew")
        

        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

    def reset(self):
        self.querrylistbox.delete("0", "end")
        self.deactivate_ok_button()
        self.activate_back_button()
        
    def enable_all_inputs(self):
        self.team_selected_menu.configure(state="normal")
        self.match_selected_menu.configure(state="normal")
        self.user_selected_menu.configure(state="normal")
        self.club_selected_menu.configure(state="normal")
        self.competition_selected_menu.configure(state="normal")

    def querry(self,querry):
        self.querrylistbox.delete("0", "end")
        self.enable_all_inputs()
        if querry=="Mannschaft":
            self.team_selected_menu.configure(state="disabled")
            for team in self.teams:
                self.querrylistbox.insert("end", team[1].name)
        elif querry=="Match":
            self.match_selected_menu.configure(state="disabled")
            for match in self.matches:
                self.querrylistbox.insert("end", f"{match[1].shooter.name} - {match[1].date}")
        elif querry=="Schütze":
            self.user_selected_menu.configure(state="disabled")
            for user in self.users:
                self.querrylistbox.insert("end", user[1].shooter.name)
        elif querry=="Verein":
            self.club_selected_menu.configure(state="disabled")
            for club in sorted(self.clubs):
                self.querrylistbox.insert("end", club[1].name)
        elif querry=="Wettbewerb":
            self.competition_selected_menu.configure(state="disabled")
            for competition in self.competitions:
                self.querrylistbox.insert("end", competition[1].name)

    def by_team(self,team):
        querry=self.desired_querry.get()
        self.querrylistbox.delete("0", "end")
        if querry=="Match":
            pass