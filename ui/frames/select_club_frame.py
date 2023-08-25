import tkinter as tk
from tkinter import ttk
from idlelib.tooltip import Hovertip
from .default_frame import DefaultFrame


class SelectClubFrame(DefaultFrame):
    def __init__(self, container, parent):
        super().__init__(container, parent)

        options = {"padx": 5, "pady": 0}
        self.scrollbar = tk.Scrollbar(self)
        self.clublistbox = tk.Listbox(self, height=10, width=50)

        self.clublistbox.bind("<<ListboxSelect>>", self.select)
        self.clublistbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.clublistbox.yview)
        self.scrollbar.grid(column=2, row=0, sticky="wens")
        self.clublistbox.grid(columnspan=2, column=0, row=0, sticky="ew")

        self.test_label = ttk.Label(self, text="")
        self.test_label.grid(columnspan=2, column=0, row=2, sticky="nesw", **options)
        self.new_button = ttk.Button(self, text="Neuer Verein")
        self.new_button.grid(column=1, row=3, sticky="e", **options)
        Hovertip(self.new_button, "Neuen Verein anlegen")
        self.new_button.configure(command=self.new)

        self.edit_button = ttk.Button(self, text="Bearbeiten")
        self.edit_button.grid(column=2, row=3, sticky="e", **options)
        Hovertip(self.edit_button, "Verein bearbeiten")
        self.edit_button.configure(command=self.edit)
        self.columnconfigure(0, weight=1)

        # add padding to the frame and show it
        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
        self.edit_club_var = False
        self.create_new_club = False

    def select(self, event):
        self.edit_club_var = False
        self.create_new_club = False
        selection = self.clublistbox.curselection()
        if len(selection) > 0:
            n = selection[0]
            if n < len(self.clubs.clubs):
                self.club = sorted(self.clubs)[n][1]
                self.test_label.config(text=self.club.name)
                self.edit_button["state"] = "normal"
            else:
                pass
                # self.edit_shooter = True
                # self.test_label.config(text="Neuer Schütze")
                # self.edit_button["state"] = "disabled"
        self.activate_back_button()
        self.activate_ok_button()

    def reset(self):
        self.test_label.config(text="Verein auswählen")
        self.club = None

        self.clublistbox.delete("0", "end")

        for club in sorted(self.clubs):
            self.clublistbox.insert("end", club[1].name)

        # self.clublistbox.insert("end", "Neuer Schütze")
        self.clublistbox.bind("<<ListboxSelect>>", self.select)
        self.deactivate_back_button()
        self.deactivate_ok_button()
        self.edit_button["state"] = "disabled"

    def edit_club(self):
        self.clublistbox.unbind("<<ListboxSelect>>")
        return self.edit_club_var

    def new_club(self):
        self.clublistbox.unbind("<<ListboxSelect>>")
        return self.create_new_club

    def edit(self):
        self.edit_club_var = True
        self.proceed()

    def new(self):
        self.club = None
        self.create_new_club = True
        self.proceed()
