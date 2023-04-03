import tkinter as tk
from tkinter import ttk
import os


# Not used yet
class SelectMatchFrame(tk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        self.matchconfig = parent.matchconfig

        options = {"padx": 5, "pady": 0}
        self.scrollbar = tk.Scrollbar(self)
        self.matchlistbox = tk.Listbox(self, height=10, width=50)
        self.matchlistbox.bind("<<ListboxSelect>>", self.select)
        self.matchlistbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.matchlistbox.yview)
        self.scrollbar.grid(column=2, row=0, sticky="wens")
        self.matchlistbox.grid(columnspan=2, column=0, row=0, sticky="ew")

        self.test_label = ttk.Label(self, text="")
        self.test_label.grid(columnspan=2, column=0, row=2, sticky="nesw", **options)

        self.columnconfigure(0, weight=1)

        # add padding to the frame and show it
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")
        # self.grid_rowconfigure(0,weight=1)
        if not os.path.exists(self.parent.matchconfigpath):
            self.parent.matchconfig["TrainingLG40"] = {
                "name": "Training LG 40",
                "schusszahl": str(40),
                "schussproserie": str(10),
                "schusswertung": "Ringe",
                "serienwertung": "Summe",
                "teilnehmerwertung": "Summe",
                "wettkampfwertung": "Maximum",
            }
            with open(self.parent.matchconfigpath, "w") as configfile:
                self.parent.matchconfig.write(configfile)
        self.parent.matchconfig.read(self.parent.matchconfigpath)

    def select(self, event):
        # self.parent.matchsection = ""
        wahl = self.matchlistbox.curselection()
        if len(wahl) > 0:
            if wahl[0] < len(self.matchconfig.sections()):
                self.parent.matchsection = self.matchconfig.sections()[wahl[0]]
            else:
                self.parent.matchsection = "Neuer Wettbewerb"

        self.test_label.config(text=self.parent.matchsection)
        self.parent.back_button["state"] = "normal"
        self.parent.ok_button["state"] = "normal"
        print(self.parent.matchsection)

    def reset(self, back=False):
        self.test_label.config(text="Wettkampf auswählen")

        self.matchlistbox.delete("0", "end")

        for section in self.matchconfig.sections():
            self.matchlistbox.insert("end", self.matchconfig.get(section, "name"))

        self.matchlistbox.bind("<<ListboxSelect>>", self.select)
        self.parent.back_button["state"] = "disabled"
        self.parent.ok_button["state"] = "disabled"

    def add_option(self):
        self.matchlistbox.insert("end", "Neuer Wettbewerb")
