import os
from tkinter import ttk
from datetime import datetime

import pdfgenerator
from idlelib.tooltip import Hovertip


class CompetitionResultFrame(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        self.label_list = []
        # field options
        options = {"padx": 5, "pady": 0}
        # user input
        self.generate_button = ttk.Button(
            self, text="Drucken / Speichern", command=self.actionSpeichern
        )
        Hovertip(
            self.generate_button,
            "Ergebnis speichern\nDas Ergebnis wird gespeichert und ein druckbarer Bericht geöffnet",
        )
        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

    def actionSpeichern(self):
        self.actionPDF()

    def actionPDF(self):
        filedate = datetime.strptime(self.parent.competition.settings.date, "%d.%m.%Y")
        filepath = self.parent.competition.settings.name.replace(" ", "_")
        filename = f"""{datetime.strftime(filedate, "%y%m%d")}_{self.parent.competition.settings.type_of_target}"""
        pdfgenerator.PDFgen.makeCompetionPDF(
            self.parent.competition,
            filepath,
            filename,
        )
        self.generate_button["state"] = "disabled"

    def remove_current_competition(self):
        self.parent.competitions.remove(self.parent.competition)
        self.parent.competition = None

    def reset(self, back=False):
        self.generate_button["state"] = "normal"
        self.parent.ok_button["state"] = "normal"
        for label in self.label_list:
            label.destroy()
        for n, entry in enumerate(self.parent.competition.entries):
            rank_label = ttk.Label(self, text=f"{n+1}")
            rank_label.grid(row=n, column=0)
            self.label_list.append(rank_label)
            name_label = ttk.Label(self, text=f"{entry.settings.shooter.name}")
            name_label.grid(row=n, column=1)
            self.label_list.append(name_label)
            result_label = ttk.Label(self, text=f"{entry.result}")
            result_label.grid(row=n, column=2)
            self.label_list.append(result_label)
        self.generate_button.grid(row=n + 1, column=0, columnspan=3, sticky="se")
        print(self.parent.competition.to_json())
