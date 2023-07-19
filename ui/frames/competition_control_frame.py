import os
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from idlelib.tooltip import Hovertip
from data.competition import Competition


class CompetitionControlFrame(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        # field options
        options = {"padx": 5, "pady": 0}
        self.columnconfigure(0, weight=1)
        # Wettkampfsteuerung
        self.general_competition_labelframe = ttk.LabelFrame(
            self, text="Wettkampfsteuerung"
        )
        self.general_competition_labelframe.columnconfigure(1, weight=1)
        self.add_competition_button = ttk.Button(
            self.general_competition_labelframe,
            text="Wettbewerb hinzufügen",
            command=self.add_competition,
        )
        self.add_competition_button.grid(row=0, column=1, sticky="e")
        Hovertip(self.add_competition_button, "Fügt einen neuen Wettbewerb hinzu")
        self.load_competition_button = ttk.Button(
            self.general_competition_labelframe,
            text="Wettbewerb laden",
            command=self.load_competition,
        )
        self.load_competition_button.grid(row=1, column=1, sticky="e")
        self.load_competition_button["state"] = "normal"
        Hovertip(
            self.load_competition_button,
            "Lädt einen gespeicherten Wettbewerb",
        )
        self.general_competition_labelframe.grid(row=0, column=0, sticky="ew")

        # Aktueller Wettkampf
        self.current_competition_labelframe = ttk.LabelFrame(
            self, text="Aktueller Wettkampf"
        )
        self.current_competition_labelframe.columnconfigure(2, weight=1)
        ttk.Label(self.current_competition_labelframe, text="Name:").grid(
            row=0, column=0, sticky="e"
        )
        ttk.Label(self.current_competition_labelframe, text="Beiträge:").grid(
            row=1, column=0, sticky="e"
        )
        self.competition_name_label = ttk.Label(
            self.current_competition_labelframe, text="-"
        )
        self.competition_name_label.grid(row=0, column=1, sticky="w")
        self.competition_count_label = ttk.Label(
            self.current_competition_labelframe, text="0"
        )
        self.competition_count_label.grid(row=1, column=1, sticky="w")
        self.add_entry_button = ttk.Button(
            self.current_competition_labelframe,
            text="Beitrag hinzufügen",
            command=self.add_entry,
        )
        self.add_entry_button.grid(row=0, column=2, sticky="e")
        Hovertip(
            self.add_entry_button,
            "Dem aktuellen Wettbewerb einen weitern Beitrag hinzufügen",
        )
        self.show_entries_button = ttk.Button(
            self.current_competition_labelframe,
            text="Teilnehmer anzeigen",
            command=self.show_entries,
        )
        self.show_entries_button.grid(row=1, column=2, sticky="e")
        self.show_entries_button["state"] = "disabled"
        Hovertip(self.show_entries_button, "Zeigt die vorhandenen Ergebnisse an")
        self.save_competition_button = ttk.Button(
            self.current_competition_labelframe,
            text="Wettkampf speichern",
            command=self.save_competition,
        )
        self.save_competition_button["state"] = "disabled"
        self.save_competition_button.grid(row=2, column=2, sticky="e")
        Hovertip(self.save_competition_button, "Den aktuellen Wettkampf speichern")
        self.finish_competition_button = ttk.Button(
            self.current_competition_labelframe,
            text="Wettbewerb beenden",
            command=self.finish_competition,
        )
        self.finish_competition_button.grid(row=3, column=2, sticky="e")
        self.finish_competition_button["state"] = "disabled"
        Hovertip(self.finish_competition_button, "Beendet den aktuellen Wettbewerb")
        self.current_competition_labelframe.grid(row=1, column=0, sticky="ew")

        # Allgemeines
        self.general_labelframe = ttk.LabelFrame(self, text="Allgemeines")
        self.general_labelframe.columnconfigure(1, weight=1)
        self.quick_analysis_button = ttk.Button(
            self.general_labelframe,
            text="Schnellauswertung",
            command=self.quick_analysis,
        )
        self.quick_analysis_button.grid(row=0, column=1, sticky="e")
        self.quick_analysis_button.configure(command=self.quick_analysis)
        Hovertip(
            self.quick_analysis_button,
            "Schnellauswertung\n Das Ergebnis wird keinem Wettbewerb hinzugefügt",
        )
        self.quit_button = ttk.Button(
            self.general_labelframe, text="Programm beenden", command=self.quit
        )
        self.quit_button.grid(row=1, column=1, sticky="e")
        Hovertip(
            self.quit_button,
            "Programm beenden",
        )

        self.general_labelframe.grid(row=3, column=0, sticky="ew")

        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

    def add_competition(self):
        self.next_step = "add competition"
        self.parent.actionOK()

    def finish_competition(self):
        self.next_step = "finish competition"
        self.parent.actionOK()

    def add_entry(self):
        self.next_step = "add entry"
        self.parent.actionOK()

    def quick_analysis(self):
        self.next_step = "quick analysis"
        self.parent.actionOK()

    def quit(self):
        MsgBox = messagebox.askquestion(
            "Wirklich beenden?",
            "Nicht gespeicherte Ergebnisse gehen verloren!",
            icon="error",
        )
        if MsgBox == "yes":
            self.next_step = "quit"
            self.parent.actionOK()

    def show_entries(self):
        self.next_step = "show entries"
        self.parent.actionOK()

    def load_competition(self):
        input_path = filedialog.askopenfilename(
            initialdir="./",
            filetypes=[("JSON-Datei", ".json")],
        )
        if os.path.isfile(input_path):
            with open(input_path, "r") as file:
                try:
                    competition = Competition.from_json(file.read())
                    self.parent.competitions.append(competition)
                    self.parent.competition = competition
                    self.reset()
                    return
                except:
                    pass
        MsgBox = messagebox.askretrycancel(
            "Keine gültige Datei ausgewählt", "Es wurde keine gültige Datei ausgeählt"
        )
        if MsgBox:
            self.load_competition()

    def save_competition(self):
        output_path = filedialog.asksaveasfilename(
            confirmoverwrite=True,
            defaultextension=".json",
            filetypes=[("JSON-Datei", ".json")],
            initialfile=f"{self.parent.competition.settings.name}".title().replace(
                " ", ""
            ),
            initialdir="./",
        )
        if output_path:
            with open(output_path, "w") as file:
                file.write(self.parent.competition.to_json())
            self.parent.competitions.remove(self.parent.competition)
            self.parent.competition = None
            self.reset()
        else:
            MsgBox = messagebox.askretrycancel(
                "Keine Datei ausgewählt", "Es wurde keine Datei ausgeählt"
            )
            if MsgBox:
                self.save_competition()

    def reset(self, back=False):
        self.parent.ok_button["state"] = "disabled"
        self.parent.back_button["state"] = "disabled"
        self.parent.competitions_frame.competition_listbox.configure(state="normal")
        self.parent.competitions_frame.update_competitions()
        self.finish_competition_button["state"] = "disabled"
        self.save_competition_button["state"] = "disabled"
        self.show_entries_button["state"] = "disabled"
        self.add_entry_button["state"] = "disabled"
        self.competition_name_label.config(text="-")
        self.competition_count_label.config(text="-")

        if not self.parent.add_to_current_competition:
            self.parent.competition = None
            self.parent.add_to_current_competition = True

        if self.parent.competitions:
            if self.parent.competition:
                self.add_entry_button["state"] = "normal"
                self.save_competition_button["state"] = "normal"
                self.competition_name_label.config(
                    text=self.parent.competition.settings.name
                )
                self.competition_count_label.config(
                    text=len(self.parent.competition.entries)
                )
                if self.parent.competition.entries:
                    self.finish_competition_button["state"] = "normal"
                    self.show_entries_button["state"] = "normal"
