import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from datetime import date
from idlelib.tooltip import Hovertip
from data.match import RADIUS_DICT
from data.competition import Competition, CompetitionSettings


class CompetitionSettingsFrame(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        # field options
        options = {"padx": 5, "pady": 0}

        # constant labels
        ttk.Label(self, text="Name:").grid(column=0, row=0, sticky="e", **options)
        ttk.Label(self, text="Datum:").grid(column=0, row=1, sticky="e", **options)
        ttk.Label(self, text="Schusszahl:").grid(column=0, row=2, sticky="e", **options)
        ttk.Label(self, text="Schuss pro Scheibe:").grid(
            column=0, row=3, sticky="e", **options
        )
        ttk.Label(self, text="Scheibentyp:").grid(
            column=0, row=4, sticky="e", **options
        )
        ttk.Label(self, text="Zehntelwertung:").grid(
            column=0, row=5, sticky="e", **options
        )

        self.name = tk.StringVar()
        self.name_entry = ttk.Entry(self, textvariable=self.name)
        self.name_entry.grid(column=1, row=0, sticky="w", **options)
        Hovertip(
            self.name_entry,
            "Name des Bewerbs, z.B.\nTraining\nLigawettkampf\nPreisschießen",
        )

        self.date = tk.StringVar()
        self.date_entry = ttk.Entry(self, textvariable=self.date)
        self.date_entry.grid(column=1, row=1, sticky="w", **options)
        Hovertip(self.date_entry, "Datum des Bewerbs")

        self.count = tk.StringVar()
        self.count_entry = ttk.Entry(self, textvariable=self.count)
        self.count_entry.grid(column=1, row=2, sticky="w", **options)
        Hovertip(
            self.count_entry,
            "Anzahl der zu wertenden Schüsse",
        )

        self.shots_per_target = tk.StringVar()
        self.shots_per_target_entry = ttk.Entry(
            self, textvariable=self.shots_per_target
        )
        self.shots_per_target_entry.grid(column=1, row=3, sticky="w", **options)
        Hovertip(
            self.shots_per_target_entry,
            "Anzahl der Schüsse pro Scheibe\nNur bei Maschinenauswertung erforderlich\nMinimum: 1\nMaximum: 5",
        )

        self.type_of_target = tk.StringVar()
        self.type_of_target_menu = tk.OptionMenu(
            self, self.type_of_target, *list(RADIUS_DICT.keys())
        )
        self.type_of_target_menu.grid(column=1, row=4, sticky="w", **options)
        Hovertip(
            self.type_of_target_menu,
            "Art der Scheibe / Disziplin",
        )

        self.decimal = tk.BooleanVar()
        self.decimal_box = tk.Checkbutton(self)
        self.decimal_box["text"] = "Zehntelwertung"
        self.decimal_box["variable"] = self.decimal
        self.decimal_box.grid(column=1, row=5, sticky="w", **options)
        Hovertip(self.decimal_box, "Wertung in Zehntelringen")

        # add padding to the frame and show it
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

    def reset(self, back=False):
        self.name.set("Training")
        self.date.set(date.today().strftime("%d.%m.%Y"))
        self.count.set("40")
        self.shots_per_target.set("1")
        self.type_of_target.set("LG")
        self.decimal.set(False)

        self.parent.back_button["state"] = "normal"
        self.parent.ok_button["state"] = "normal"

    def parseInput(self):
        name = self.name.get()
        decimal = self.decimal.get()
        type_of_target = self.type_of_target.get()
        if type_of_target == "":
            showerror(
                title="Scheibentyp auswählen",
                message="Kein gültiger Scheibentyp ausgewählt",
            )
            return False
        date = self.date.get()

        try:
            count = int(self.count.get())
        except ValueError as error:
            showerror(title="Das ist keine Zahl", message=error)
            return False

        try:
            shots_per_target = int(self.shots_per_target.get())
        except ValueError as error:
            showerror(title="Das ist keine Zahl", message=error)
            return False
        self.parent.competitions.append(
            Competition(
                CompetitionSettings(
                    name=name,
                    date=date,
                    count=count,
                    shots_per_target=shots_per_target,
                    type_of_target=type_of_target,
                    decimal=decimal,
                )
            )
        )
        self.parent.competition = self.parent.competitions[-1]
        self.parent.competitions_frame.competition_listbox.configure(state="normal")
        self.parent.competitions_frame.update_competitions()
        self.parent.competitions_frame.competition_listbox.configure(state="disabled")
        return True
