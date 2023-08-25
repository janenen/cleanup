import tkinter as tk
from tkinter import ttk
from data.user import User
from idlelib.tooltip import Hovertip
from .default_frame import DefaultFrame


class SelectUserFrame(DefaultFrame):
    def __init__(self, container, parent):
        super().__init__(container, parent)
        options = {"padx": 5, "pady": 0}
        self.scrollbar = tk.Scrollbar(self)
        self.userlistbox = tk.Listbox(self, height=10, width=50)

        def onselect(event):
            self.select()

        self.userlistbox.bind("<<ListboxSelect>>", onselect)
        self.userlistbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.userlistbox.yview)
        self.scrollbar.grid(column=4, row=0, sticky="wens")
        self.userlistbox.grid(columnspan=4, column=0, row=0, sticky="ew")

        ttk.Label(self, text="Name: ").grid(column=0, row=1, sticky="nesw", **options)
        self.name_label = ttk.Label(self, text="")
        self.name_label.grid(column=1, row=1, sticky="w", **options)

        ttk.Label(self, text="Verein: ").grid(column=0, row=2, sticky="nesw", **options)
        self.club_label = ttk.Label(self, text="")
        self.club_label.grid(column=1, row=2, sticky="nesw", **options)
        self.club_button = ttk.Button(self, text="Auswählen")
        self.club_button.grid(column=3, row=2, sticky="w", **options)
        Hovertip(self.club_button, "Verein auswählen")

        ttk.Label(self, text="Mannschaft: ").grid(
            column=0, row=3, sticky="nesw", **options
        )
        self.team_label = ttk.Label(self, text="")
        self.team_label.grid(column=1, row=3, sticky="nesw", **options)
        self.club_button.configure(command=self.select_club)

        self.team_button = ttk.Button(self, text="Auswählen")
        self.team_button.grid(column=3, row=3, sticky="w", **options)
        Hovertip(self.team_button, "Mannschaft auswählen")
        self.team_button.configure(command=self.select_team)

        self.new_button = ttk.Button(self, text="Neuer Benutzer")
        self.new_button.grid(column=2, row=1, sticky="e", **options)
        Hovertip(self.new_button, "Neuen Benutzer anlegen")
        self.new_button.configure(command=self.new)

        self.edit_button = ttk.Button(self, text="Bearbeiten")
        self.edit_button.grid(column=3, row=1, sticky="e", **options)
        Hovertip(self.edit_button, "Benutzer bearbeiten")
        self.edit_button.configure(command=self.edit)
        self.columnconfigure(1, weight=1)

        # add padding to the frame and show it
        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
        self.select_team_var = False
        self.select_club_var = False
        self.edit_shooter = False
        self.create_new_user = False

    def select(self, event):
        self.edit_shooter = False
        self.create_new_user = False
        selection = self.userlistbox.curselection()
        if len(selection) > 0:
            n = selection[0]
            if n < len(self.users.users):
                self.user = sorted(self.users)[n][1]
                self.name_label.config(text=self.user.name)
                self.club_label.config(text=self.club.name if self.club else "")
                self.team_label.config(text=self.team.name if self.team else "")
                self.edit_button["state"] = "normal"
                self.club_button["state"] = "normal"
                self.team_button["state"] = "normal"
            else:
                pass

        self.activate_back_button()
        self.activate_ok_button()

    def reset(self):
        self.name_label.config(
            text=self.user.name if self.user else "Schütze auswählen"
        )
        self.club_label.config(text=self.club.name if self.club else "-")
        self.club_button["state"] = "normal" if self.user else "disabled"
        self.team_label.config(text=self.team.name if self.team else "-")
        self.team_button["state"] = "normal" if self.user else "disabled"
        self.userlistbox.delete("0", "end")

        for user in sorted(self.users):
            self.userlistbox.insert("end", user[1].name)

        self.userlistbox.bind("<<ListboxSelect>>", self.select)
        # self.deactivate_back_button()
        if not self.user:
            self.deactivate_ok_button()
        else:
            self.activate_ok_button()
        self.edit_button["state"] = "disabled"

    def edit_user(self):
        self.userlistbox.unbind("<<ListboxSelect>>")
        return self.edit_shooter

    def new_user(self):
        self.userlistbox.unbind("<<ListboxSelect>>")
        return self.create_new_user

    def edit(self):
        self.edit_shooter = True
        self.proceed()

    def new(self):
        self.user = None
        self.create_new_user = True
        self.proceed()

    def team_to_select(self):
        if self.select_team_var == True:
            self.select_team_var = False
            return True
        else:
            return False

    def select_team(self):
        self.select_team_var = True
        self.proceed()

    def club_to_select(self):
        if self.select_club_var == True:
            self.select_club_var = False
            return True
        else:
            return False

    def select_club(self):
        self.select_club_var = True
        self.proceed()
