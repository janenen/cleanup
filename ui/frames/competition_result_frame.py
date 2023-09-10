import os
import sys
import tempfile
from tkinter import ttk
from datetime import datetime

from fpdf import FPDF
from data.competition import SORTING_FUNCTION
from data.match import Match
from idlelib.tooltip import Hovertip
from .default_frame import DefaultFrame


class CompetitionResultFrame(DefaultFrame):
    def __init__(self, container, parent):
        super().__init__(container, parent)

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
        self._makeCompetionPDF()
        self.generate_button["state"] = "disabled"

    def remove_current_competition(self):
        self.competition.active = False
        self.competitions.save()
        self.active_competitions.remove(self.competition)
        self.competition = None

    def get_sorted_results(self) -> list[Match]:
        return sorted(
            [self.matches[key] for key in self.competition.entries],
            key=SORTING_FUNCTION[self.competition.modus]["key"],
            reverse=SORTING_FUNCTION[self.competition.modus]["reverse"],
        )

    def _makeCompetionPDF(self):
        filedate = datetime.strptime(self.competition.date, "%d.%m.%Y")
        filepath = self.competition.name.replace(" ", "_")
        filename = f"""{datetime.strftime(filedate, "%y%m%d")}_{self.competition.type_of_target}"""
        outdir = os.getcwd()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        # pdf.set_font('Helvetica','',10)
        pdf.text(
            10,
            20,
            f"Ergebnisliste {self.competition.name} {self.competition.date}",
        )
        pdf.set_font("Helvetica", "", 10)

        # create a temporary directory
        with tempfile.TemporaryDirectory() as directory:
            for n, entry in enumerate(self.get_sorted_results()):
                pdf.text(10, 30 + n * 5, str(n + 1) + ".")
                pdf.text(15, 30 + n * 5, entry.shooter.name)
                for j, series in enumerate(entry.series):
                    pdf.text((190 - 120) + j * 10, 30 + n * 5, f"{series.summe_ganz}")
                pdf.text(
                    190, 30 + n * 5, str(entry.get_result(self.competition.decimal))
                )
        newpath = os.path.join(outdir, "output", "competitions", filepath)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        testfilename = f"{filename}.pdf"
        n = 1
        while os.path.exists(os.path.join(newpath, testfilename)):
            testfilename = f"{filename}_{n}.pdf"
            n += 1
        pdf.output(os.path.join(newpath, testfilename), "F")

        if not sys.platform == "linux":
            os.startfile(os.path.join(newpath, testfilename))

    def reset(self):
        self.generate_button["state"] = "normal"
        self.activate_ok_button()
        for label in self.label_list:
            label.destroy()
        for n, entry in enumerate(self.get_sorted_results()):
            rank_label = ttk.Label(self, text=f"{n+1}")
            rank_label.grid(row=n, column=0)
            self.label_list.append(rank_label)
            name_label = ttk.Label(self, text=f"{entry.shooter.name}")
            name_label.grid(row=n, column=1)
            self.label_list.append(name_label)
            result_label = ttk.Label(
                self, text=f"{entry.get_result(self.competition.decimal)}"
            )
            result_label.grid(row=n, column=2)
            self.label_list.append(result_label)
        self.generate_button.grid(row=n + 1, column=0, columnspan=3, sticky="se")
