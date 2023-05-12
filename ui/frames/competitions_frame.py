import tkinter as tk
from tkinter import ttk


class Competitions(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        self.competition_listbox = tk.Listbox(self, height=14, width=25)

        self.competition_listbox.grid(column=0, row=0, sticky="nesw")
        # add padding to the frame and show it
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def select(self, event):
        selection = self.competition_listbox.curselection()
        print(selection)
        if len(selection) > 0:
            n = selection[0]
        if self.showing == "competitions":
            self.parent.competition = self.parent.competitions[n]
            print(self.parent.competition.settings.name)
        elif self.showing == "entries":
            self.parent.current_match = self.parent.competition.entries[n]
        self.parent.frame.reset()

    def update_competitions(self):
        self.showing = "competitions"
        self.competition_listbox.delete("0", "end")
        for comp in self.parent.competitions:
            self.competition_listbox.insert("end", comp.settings.name)
        self.competition_listbox.bind("<<ListboxSelect>>", self.select)

    def update_entries(self):
        self.showing = "entries"
        self.competition_listbox.delete("0", "end")
        for entry in self.parent.competition.entries:
            self.competition_listbox.insert("end", entry.settings.shooter.name)
        self.competition_listbox.bind("<<ListboxSelect>>", self.select)
