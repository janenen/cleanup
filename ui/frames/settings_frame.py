import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from datetime import date
from idlelib.tooltip import Hovertip
from shot import Match


class SettingsFrame(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        # field options
        options = {"padx": 5, "pady": 0}

        # constant labels
        ttk.Label(self, text="Bewerb:").grid(column=0, row=0, sticky="e", **options)
        ttk.Label(self, text="Name:").grid(column=0, row=1, sticky="e", **options)
        ttk.Label(self, text="Verein:").grid(column=0, row=2, sticky="e", **options)
        ttk.Label(self, text="Datum:").grid(column=0, row=3, sticky="e", **options)
        ttk.Label(self, text="Schusszahl:").grid(column=0, row=4, sticky="e", **options)
        ttk.Label(self, text="Schuss pro Scheibe:").grid(
            column=0, row=5, sticky="e", **options
        )
        ttk.Label(self, text="Scheibentyp:").grid(
            column=0, row=6, sticky="e", **options
        )
        ttk.Label(self, text="Quelle:").grid(column=0, row=7, sticky="e", **options)
        # ttk.Label(self, text="Zehntelwertung:").grid(column=0,row=6,sticky="e",**options)

        # user input
        self.bewerb = tk.StringVar()
        self.bewerb_entry = ttk.Entry(self, textvariable=self.bewerb)
        self.bewerb_entry.grid(column=1, row=0, sticky="w", **options)
        self.bewerb_entry.focus()
        Hovertip(
            self.bewerb_entry,
            "Art des Bewerbs, z.B.\nTraining\nLigawettkampf\nPreisschießen",
        )

        self.name = tk.StringVar()
        self.name_entry = ttk.Entry(self, textvariable=self.name)
        self.name_entry.grid(column=1, row=1, sticky="w", **options)
        Hovertip(self.name_entry, "Name des Schützen")

        self.verein = tk.StringVar()
        self.verein_entry = ttk.Entry(self, textvariable=self.verein)
        self.verein_entry.grid(column=1, row=2, sticky="w", **options)
        Hovertip(self.verein_entry, "Verein des Schützen")

        self.datum = tk.StringVar()
        self.datum_entry = ttk.Entry(self, textvariable=self.datum)
        self.datum_entry.grid(column=1, row=3, sticky="w", **options)
        Hovertip(self.datum_entry, "Datum des Bewerbs")

        self.anzahl = tk.StringVar()
        self.anzahl_entry = ttk.Entry(self, textvariable=self.anzahl)
        self.anzahl_entry.grid(column=1, row=4, sticky="w", **options)
        Hovertip(
            self.anzahl_entry,
            "Anzahl der zu wertenden Schüsse\nNur bei Maschinenauswertung erforderlich\nMinimum: 1\nMaximum: 200",
        )

        self.proscheibe = tk.StringVar()
        self.proscheibe_entry = ttk.Entry(self, textvariable=self.proscheibe)
        self.proscheibe_entry.grid(column=1, row=5, sticky="w", **options)
        Hovertip(
            self.proscheibe_entry,
            "Anzahl der Schüsse pro Scheibe\nNur bei Maschinenauswertung erforderlich\nMinimum: 1\nMaximum: 5",
        )

        self.scheibentyp = tk.StringVar()
        self.scheibentyp_menu = tk.OptionMenu(
            self, self.scheibentyp, *list(Match.radius_dict.keys())
        )
        self.scheibentyp_menu.grid(column=1, row=6, sticky="w", **options)
        Hovertip(
            self.scheibentyp_menu,
            "Art der Scheibe / Disziplin\nNur zum Einlesen von .qsd-Dateien notwendig",
        )

        self.quelle_label = ttk.Label(self, text="")
        self.quelle_label.grid(column=1, row=7, sticky="w", **options)

        self.zehntel = tk.BooleanVar()
        self.zehntel_box = tk.Checkbutton(self)
        self.zehntel_box["text"] = "Zehntelwertung"
        self.zehntel_box["variable"] = self.zehntel
        self.zehntel_box.grid(column=1, row=8, sticky="w", **options)
        Hovertip(self.zehntel_box, "Wertung in Zehntelringen")

        self.ext_analysis = tk.BooleanVar()
        self.ext_analysis_box = tk.Checkbutton(self)
        self.ext_analysis_box["text"] = "Erweiterte Analyse"
        self.ext_analysis_box["variable"] = self.ext_analysis
        self.ext_analysis_box.grid(column=1, row=9, sticky="w", **options)
        Hovertip(
            self.ext_analysis_box, "Aktiviert die erweiterte Analyse in der PDF-Datei"
        )

        self.save = tk.BooleanVar()
        self.save_box = tk.Checkbutton(self)
        self.save_box["text"] = "Speichern"
        self.save_box["variable"] = self.save
        self.save_box.grid(column=1, row=10, sticky="w", **options)
        Hovertip(self.save_box, "Daten des Schützen und Einstellungen speichern")

        # add padding to the frame and show it
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def reset(self, back=False):
        self.parent.match = Match()
        self.name.set(self.parent.userconfig.get(self.parent.usersection, "Name"))
        self.verein.set(self.parent.userconfig.get(self.parent.usersection, "Verein"))
        self.bewerb.set(self.parent.userconfig.get(self.parent.usersection, "Bewerb"))
        self.datum.set(date.today().strftime("%d.%m.%Y"))
        self.anzahl.set(
            self.parent.userconfig.get(self.parent.usersection, "Schusszahl")
        )
        self.proscheibe.set(
            self.parent.userconfig.get(self.parent.usersection, "SchussProScheibe")
        )
        self.zehntel.set(
            self.parent.userconfig.getboolean(self.parent.usersection, "Zehntel")
        )
        self.parent.fsk_schnitt = self.parent.userconfig.getfloat(
            self.parent.usersection, "Schnitt"
        )
        if self.parent.userconfig.has_option(self.parent.usersection, "Erweitert"):
            self.ext_analysis.set(
                self.parent.userconfig.getboolean(self.parent.usersection, "Erweitert")
            )
        else:
            self.ext_analysis.set(False)

        if self.parent.quelle == "maschine":
            self.datum_entry["state"] = "normal"
            self.anzahl_entry["state"] = "normal"
            self.proscheibe_entry["state"] = "normal"
            self.save_box["state"] = "normal"
            self.scheibentyp_menu["state"] = "disabled"
            self.quelle_label.config(text=self.parent.ser.name)
        elif self.parent.quelle == "csv":
            self.datum_entry["state"] = "disabled"
            self.anzahl_entry["state"] = "disabled"
            self.proscheibe_entry["state"] = "disabled"
            self.save_box["state"] = "disabled"
            self.scheibentyp_menu["state"] = "disabled"
            self.quelle_label.config(text=self.parent.inputfile)
        elif self.parent.quelle == "string":
            self.datum_entry["state"] = "disabled"
            self.anzahl_entry["state"] = "disabled"
            self.proscheibe_entry["state"] = "disabled"
            self.save_box["state"] = "disabled"
            self.scheibentyp_menu["state"] = "disabled"
            self.quelle_label.config(text="QR-Code")
        else:  # qsd
            self.datum_entry["state"] = "normal"
            self.anzahl_entry["state"] = "disabled"
            self.proscheibe_entry["state"] = "disabled"
            self.save_box["state"] = "disabled"
            self.scheibentyp_menu["state"] = "normal"
            self.quelle_label.config(text=self.parent.inputfile)

        self.parent.back_button["state"] = "normal"
        self.parent.ok_button["state"] = "normal"

    def parseInput(self):
        self.parent.match.bewerb = self.bewerb.get()
        if self.parent.match.bewerb == "FSK":
            self.parent.fsk = True
        else:
            self.parent.fsk = False
        self.parent.match.name = self.name.get()
        self.parent.match.verein = self.verein.get()
        self.parent.match.setZehntel(self.zehntel.get())
        self.parent.is_extended = self.ext_analysis.get()
        if self.parent.quelle == "qsd":
            self.parent.match.scheibentyp = self.scheibentyp.get()
            if self.parent.match.scheibentyp == "":
                showerror(
                    title="Scheibentyp auswählen",
                    message="Kein gültiger Scheibentyp ausgewählt",
                )
                return False
        if self.parent.quelle == "maschine" or self.parent.quelle == "qsd":
            self.parent.match.datum = self.datum.get()
        if self.parent.quelle == "maschine":
            try:
                self.parent.anzahl = int(self.anzahl.get())
            except ValueError as error:
                showerror(title="Das ist keine Zahl, using default", message=error)
                return False
            try:
                self.parent.proscheibe = int(self.proscheibe.get())
            except ValueError as error:
                showerror(title="Das ist keine Zahl, using default", message=error)
                return False
            if self.parent.usersection == "Neu" and self.save.get():
                self.parent.userconfig[self.name.get().replace(" ", "")] = {
                    "Bewerb": self.parent.match.bewerb,
                    "Name": self.parent.match.name,
                    "Verein": self.parent.match.verein,
                    "Schusszahl": str(self.parent.anzahl),
                    "SchussProScheibe": str(self.parent.proscheibe),
                    "Zehntel": str(self.parent.match.zehntel),
                    "Schnitt": self.parent.userconfig.get("DEFAULT", "Schnitt"),
                    "Erweitert": str(self.parent.is_extended),
                    "niceness": "0",
                }
                with open(self.parent.userconfigpath, "w") as configfile:
                    self.parent.userconfig.write(configfile)
                self.parent.usersection = self.name.get().replace(" ", "")
            elif self.save.get():
                if self.parent.userconfig.has_option(
                    self.parent.usersection, "niceness"
                ):
                    old_niceness = self.parent.userconfig[self.parent.usersection][
                        "niceness"
                    ]
                else:
                    old_niceness = "0"
                self.parent.userconfig[self.parent.usersection] = {
                    "Bewerb": self.parent.match.bewerb,
                    "Name": self.parent.match.name,
                    "Verein": self.parent.match.verein,
                    "Schusszahl": str(self.parent.anzahl),
                    "SchussProScheibe": str(self.parent.proscheibe),
                    "Zehntel": str(self.parent.match.zehntel),
                    "Erweitert": str(self.parent.is_extended),
                    "niceness": old_niceness,
                }
                with open(self.parent.userconfigpath, "w") as configfile:
                    self.parent.userconfig.write(configfile)
        return True
