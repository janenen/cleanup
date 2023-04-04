import configparser
import tkinter as tk
from tkinter import ttk
import os
from data.shooter import Shooter


class SelectUserFrame(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        self.userconfig = configparser.ConfigParser()
        self.usersection = ""
        self.userconfigpath = "./schuetzen.ini"

        options = {"padx": 5, "pady": 0}
        self.scrollbar = tk.Scrollbar(self)
        self.userlistbox = tk.Listbox(self, height=10, width=50)

        def onselect(event):
            self.select()

        self.userlistbox.bind("<<ListboxSelect>>", onselect)
        self.userlistbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.userlistbox.yview)
        self.scrollbar.grid(column=2, row=0, sticky="wens")
        self.userlistbox.grid(columnspan=2, column=0, row=0, sticky="ew")

        self.test_label = ttk.Label(self, text="")
        self.test_label.grid(columnspan=2, column=0, row=2, sticky="nesw", **options)

        self.columnconfigure(0, weight=1)

        # add padding to the frame and show it
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def select(self, event):
        self.new_shooter = False
        selection = self.userlistbox.curselection()

        if len(selection) > 0:
            n = selection[0]
            if n < len(self.userconfig.sections()):
                self.usersection = sorted(
                    self.userconfig.sections(), key=self.get_niceness, reverse=True
                )[n]
                self.test_label.config(
                    text=self.userconfig.get(self.usersection, "Name")
                )
            else:
                self.new_shooter = True
                self.test_label.config(text="Neuer Schütze")
        self.parent.back_button["state"] = "normal"
        self.parent.ok_button["state"] = "normal"

    def reset(self, back=False):
        self.test_label.config(text="Schütze auswählen")

        if not os.path.exists(self.userconfigpath):
            self.userconfig["DEFAULT"] = {
                "Name": "Neuer Schütze",
                "Verein": "",
                "Mannschaft": "",
                "niceness": "0",
            }
            with open(self.userconfigpath, "w") as configfile:
                self.userconfig.write(configfile)
        self.userconfig.read(self.userconfigpath)

        self.userlistbox.delete("0", "end")

        for section in sorted(
            self.userconfig.sections(), key=self.get_niceness, reverse=True
        ):
            self.userlistbox.insert("end", self.userconfig.get(section, "Name"))
        self.userlistbox.insert("end", "Neuer Schütze")
        self.userlistbox.bind("<<ListboxSelect>>", self.select)
        self.parent.back_button["state"] = "disabled"
        self.parent.ok_button["state"] = "disabled"

    def get_niceness(self, section):
        if self.userconfig.has_option(section, "niceness"):
            return self.userconfig.getint(section, "niceness")
        else:
            return 0

    def new_user(self):
        self.userlistbox.unbind("<<ListboxSelect>>")
        if not self.new_shooter:
            self.parent.competition.add_match(
                Shooter(
                    name=self.userconfig[self.usersection]["Name"],
                    club=self.userconfig[self.usersection]["Verein"],
                    team=None,
                )
            )
        return self.new_shooter
