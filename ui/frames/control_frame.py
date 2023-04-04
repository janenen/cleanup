import tkinter as tk
from tkinter import ttk
from data.competition import Competition
from ui.frames.select_user_frame import SelectUserFrame
from ui.frames.reading_frame import ReadingFrame
from ui.frames.settings_frame import UserSettingsFrame
from ui.frames.machine_selection_frame import MaschineSelectionFrame
from ui.frames.user_result_frame import UserResultFrame
from ui.frames.competition_settings_frame import CompetitionSettingsFrame
from ui.frames.competition_result_frame import CompetitionResultFrame


class ControlFrame(ttk.Frame):
    def actionOK(self):
        back = False
        if self.nextframe == "competition":
            if self.frames["competition"].parseInput():
                self.nextframe = "machine"

        elif self.nextframe == "machine":
            self.nextframe = "user"

        # loop while no new entry is available
        elif self.nextframe == "user":
            if self.frames["user"].new_user():
                self.nextframe = "user_settings"
            else:
                self.nextframe = "reading"

        elif self.nextframe == "user_settings":
            if self.frames["user_settings"].parseInput():
                self.nextframe = "reading"

        elif self.nextframe == "reading":
            self.nextframe = "match_result"

        elif self.nextframe == "match_result":
            MsgBox = tk.messagebox.askquestion(
                "Weiterer Teilnehmer?",
                "Weiterer Teilnehmer hinzufügen?",
                icon="error",
            )
            if MsgBox == "yes":
                self.nextframe = "user"
            else:
                self.nextframe = "competition_result"
        elif self.nextframe == "competition_result":
            MsgBox = tk.messagebox.askquestion(
                "Programm schließen",
                "Programm schließen?\nAlles gespeichert?",
                icon="error",
            )
            if MsgBox == "yes":
                self.container.quit()
            else:
                return
        self.change_frame(back)

    def actionBack(self):
        if self.nextframe == "match_result":
            MsgBox = tk.messagebox.askquestion(
                "Alles gespeichert?",
                "Alles gespeichert?",
                icon="error",
            )
            if MsgBox == "no":
                return
        self.reset()
        self.nextframe = "competition"
        self.change_frame(back=True)

    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.nextframe = "competition"
        #  buttons
        self.back_button = ttk.Button(self, text="Zurück", command=self.actionBack)
        self.back_button.grid(column=1, row=0, padx=5, pady=5)
        self.ok_button = ttk.Button(self, text="OK", command=self.actionOK)
        self.ok_button.grid(column=2, row=0, padx=5, pady=5)
        self.grid(column=0, row=1, padx=5, pady=5, sticky="se")
        self.reset()
        # initialize frames
        self.frames = {
            "competition": CompetitionSettingsFrame(container, self),
            "machine": MaschineSelectionFrame(container, self),
            "user": SelectUserFrame(container, self),
            "user_settings": UserSettingsFrame(container, self),
            "reading": ReadingFrame(container, self),
            "match_result": UserResultFrame(container, self),
            "competition_result": CompetitionResultFrame(container, self),
        }
        self.change_frame()

    def reset(self):
        self.competition: Competition = None

    def change_frame(self, back=False):
        frame = self.frames[self.nextframe]
        frame.tkraise()
        frame.reset(back)
