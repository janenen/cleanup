import configparser
import tkinter as tk
from tkinter import ttk
import os
from data.shooter import Shooter
from data.user import User, UserSettings, UserList


class SelectUserFrame(ttk.Frame):
    userlist: UserList

    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        self.userconfigpath = "./schuetzen.ini"
        self.userjsonpath = "./users.json"

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
        print(selection)
        if len(selection) > 0:
            n = selection[0]
            if n < len(self.userlist.users):
                self.usersection: User = sorted(
                    self.userlist.users, key=self.get_niceness, reverse=True
                )[n]
                self.test_label.config(text=self.usersection.name)
            else:
                self.new_shooter = True
                self.test_label.config(text="Neuer Schütze")
        self.parent.back_button["state"] = "normal"
        self.parent.ok_button["state"] = "normal"

    def reset(self, back=False):
        self.test_label.config(text="Schütze auswählen")

        if os.path.exists(self.userjsonpath):  # case start with existing user.json
            with open(self.userjsonpath, "r") as json_file:
                self.userlist = UserList.from_json(json_file.read())

        elif os.path.exists(self.userconfigpath):  # legacy mode
            userconfig = configparser.ConfigParser()
            userconfig.read(self.userconfigpath)
            self.userlist = UserList()
            for section in userconfig.sections():
                print(section)
                if not (section == "Neu" or section == "NeuerSchütze"):
                    shooter = Shooter(
                        name=userconfig.get(section, "Name"),
                        club=userconfig.get(section, "Verein"),
                        team=None,
                    )
                    settings = UserSettings(
                        niceness=userconfig.getint(section, "niceness", fallback=0),
                        extended_analysis=userconfig.getboolean(
                            section, "erweitert", fallback=False
                        ),
                    )
                    self.userlist.users.append(User(data=shooter, settings=settings))
            with open(self.userjsonpath, "w") as json_file:
                json_file.write(self.userlist.to_json())
            # os.remove(self.userconfigpath)
        else:  # first start
            self.userlist = UserList()

        self.userlistbox.delete("0", "end")

        for user in sorted(self.userlist.users, key=self.get_niceness, reverse=True):
            self.userlistbox.insert("end", user.name)

        # for section in sorted(
        #    self.userconfig.sections(), key=self.get_niceness, reverse=True
        # ):
        #    self.userlistbox.insert("end", self.userconfig.get(section, "Name"))
        self.userlistbox.insert("end", "Neuer Schütze")
        self.userlistbox.bind("<<ListboxSelect>>", self.select)
        self.parent.back_button["state"] = "disabled"
        self.parent.ok_button["state"] = "disabled"

    def get_niceness(self, user: User):
        if user.niceness:
            return user.niceness
        else:
            return 0

    def new_user(self):
        self.userlistbox.unbind("<<ListboxSelect>>")
        if not self.new_shooter:
            self.parent.competition.add_match(
                Shooter(
                    name=self.usersection.name,
                    club=self.usersection.club,
                    team=None,
                )
            )
        return self.new_shooter
