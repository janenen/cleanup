import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
import os


class SelectUserFrame(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent

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

        # button

        # self.select_button = ttk.Button(self, text='Auswählen')
        # self.select_button.grid(column=1, row=1, sticky='e', **options)
        # self.select_button.configure(command=self.select)

        self.test_label = ttk.Label(self, text="")
        self.test_label.grid(columnspan=2, column=0, row=2, sticky="nesw", **options)

        self.columnconfigure(0, weight=1)

        # add padding to the frame and show it
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")
        # self.grid_rowconfigure(0,weight=1)

    def select(self, event):
        wahl = self.userlistbox.curselection()
        self.userlistbox.unbind("<<ListboxSelect>>")
        if len(wahl) > 0:
            n = wahl[0]
            self.parent.usersection = sorted(
                self.parent.userconfig.sections(), key=self.get_niceness, reverse=True
            )[n]

            self.test_label.config(
                text=self.parent.userconfig.get(self.parent.usersection, "Name")
            )
        self.parent.back_button["state"] = "normal"
        self.parent.ok_button["state"] = "normal"

    def reset(self, back=False):
        self.test_label.config(text="Schütze auswählen")

        if not os.path.exists(self.parent.userconfigpath):
            self.parent.userconfig["DEFAULT"] = {
                "Bewerb": "Training",
                "Name": "Neuer Schütze",
                "Verein": "",
                "Schusszahl": "40",
                "SchussProScheibe": "1",
                "Zehntel": "False",
                "Schnitt": "2",
                "Erweitert": "False",
                "niceness": "0",
            }
            self.parent.userconfig["Neu"] = {}
            with open(self.parent.userconfigpath, "w") as configfile:
                self.parent.userconfig.write(configfile)
        self.parent.userconfig.read(self.parent.userconfigpath)

        self.userlistbox.delete("0", "end")

        for section in sorted(
            self.parent.userconfig.sections(), key=self.get_niceness, reverse=True
        ):
            self.userlistbox.insert("end", self.parent.userconfig.get(section, "Name"))
        self.userlistbox.bind("<<ListboxSelect>>", self.select)
        self.parent.back_button["state"] = "disabled"
        self.parent.ok_button["state"] = "disabled"

    def get_niceness(self, section):
        if self.parent.userconfig.has_option(section, "niceness"):
            return self.parent.userconfig.getint(section, "niceness")
        else:
            return 0
