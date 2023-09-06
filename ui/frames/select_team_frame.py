import tkinter as tk
from tkinter import ttk
from idlelib.tooltip import Hovertip
from .default_frame import DefaultFrame


class SelectTeamFrame(DefaultFrame):
    def __init__(self, container, parent):
        super().__init__(container, parent)

        options = {"padx": 5, "pady": 0}
        self.scrollbar = tk.Scrollbar(self)
        self.teamlistbox = tk.Listbox(self, height=10, width=50)

        self.teamlistbox.bind("<<ListboxSelect>>", self.select)
        self.teamlistbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.teamlistbox.yview)
        self.scrollbar.grid(column=2, row=0, sticky="wens")
        self.teamlistbox.grid(columnspan=2, column=0, row=0, sticky="ew")

        self.test_label = ttk.Label(self, text="")
        self.test_label.grid(columnspan=2, column=0, row=2, sticky="nesw", **options)
        self.new_button = ttk.Button(self, text="Neue Mannschaft")
        self.new_button.grid(column=1, row=3, sticky="e", **options)
        Hovertip(self.new_button, "Neue Mannschaft anlegen")
        self.new_button.configure(command=self.new)

        self.edit_button = ttk.Button(self, text="Bearbeiten")
        self.edit_button.grid(column=2, row=3, sticky="e", **options)
        Hovertip(self.edit_button, "Mannschaft bearbeiten")
        self.edit_button.configure(command=self.edit)
        self.columnconfigure(0, weight=1)

        # add padding to the frame and show it
        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
        self.edit_team_var = False
        self.create_new_team = False

    def select(self, event):
        self.edit_shooter = False
        self.create_new_team = False
        selection = self.teamlistbox.curselection()
        if len(selection) > 0:
            n = selection[0]
            if n < len(self.teams.teams):
                self.team = sorted(self.teams)[n][1]
                self.test_label.config(text=self.team.name)
                self.edit_button["state"] = "normal"
            elif n == len(self.teams.teams):
                self.team = None
                self.test_label.config(text="Keine Mannschaft ausgewählt")
                self.edit_button["state"] = "disabled"
            else:
                return
        self.activate_back_button()
        self.activate_ok_button()

    def reset(self):
        self.test_label.config(text="Mannschaft auswählen")
        self.team = None

        self.teamlistbox.delete("0", "end")

        for team in sorted(self.teams):
            self.teamlistbox.insert("end", team[1].name)
        self.teamlistbox.insert("end", "Keine")

        # self.teamlistbox.insert("end", "Neuer Schütze")
        self.teamlistbox.bind("<<ListboxSelect>>", self.select)
        self.deactivate_back_button()
        self.deactivate_ok_button()
        self.edit_button["state"] = "disabled"

    def edit_team(self):
        self.teamlistbox.unbind("<<ListboxSelect>>")
        return self.edit_team_var

    def new_team(self):
        self.teamlistbox.unbind("<<ListboxSelect>>")
        return self.create_new_team

    def edit(self):
        self.edit_team_var = True
        self.proceed()

    def new(self):
        self.team = None
        self.create_new_team = True
        self.proceed()
