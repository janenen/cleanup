import sys
import tkinter as tk
from tkinter import ttk
from data.competition import Competition
from data.match import Match
from data.user import User, UserList
from machines.machine import Machine
from .select_user_frame import SelectUserFrame
from .reading_frame import ReadingFrame
from .settings_frame import UserSettingsFrame
from .machine_selection_frame import MaschineSelectionFrame
from .user_result_frame import UserResultFrame
from .competition_settings_frame import CompetitionSettingsFrame
from .competition_result_frame import CompetitionResultFrame
from .competitions_frame import Competitions
from .competition_control_frame import CompetitionControlFrame


class ControlFrame(ttk.Frame):
    competitions: list[Competition] = []
    competition: Competition
    userlist: UserList
    user: User = None
    current_match: Match = None
    source: Machine

    def actionOK(self):
        back = False
        if self.nextframe == "control":
            self.competitions_frame.competition_listbox.unbind("<<ListboxSelect>>")
            self.competitions_frame.competition_listbox.configure(state="disabled")
            if self.frames["control"].next_step == "add competition":
                self.nextframe = "competition"
            elif self.frames["control"].next_step == "finish competition":
                self.nextframe = "competition_result"
            elif self.frames["control"].next_step == "add entry":
                self.nextframe = "machine"
            elif self.frames["control"].next_step == "quick analysis":
                self.nextframe = "machine"
            elif self.frames["control"].next_step == "quit":
                sys.exit(0)

        elif self.nextframe == "competition":
            if self.frames["competition"].parseInput():
                self.nextframe = "machine"

        elif self.nextframe == "machine":
            self.nextframe = "user"

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
            self.competitions_frame.competition_listbox.unbind("<<ListboxSelect>>")
            self.nextframe = "control"

        elif self.nextframe == "competition_result":
            MsgBox = tk.messagebox.askquestion(
                "Alles gespeichert?",
                "Alles gespeichert?",
                icon="error",
            )
            if MsgBox == "yes":
                self.competitions_frame.competition_listbox.configure(state="normal")
                self.nextframe = "control"
                self.frame.remove_current_competition()
            else:
                return
        self.change_frame(back)

    def actionBack(self):
        self.competitions_frame.competition_listbox.configure(state="normal")
        self.nextframe = "control"
        self.change_frame(back=True)

    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.nextframe = "control"
        #  buttons
        self.back_button = ttk.Button(self, text="Zurück", command=self.actionBack)
        self.back_button.grid(column=1, row=0, padx=5, pady=5)
        self.ok_button = ttk.Button(self, text="OK", command=self.actionOK)
        self.ok_button.grid(column=2, row=0, padx=5, pady=5)
        self.grid(column=1, row=1, padx=5, pady=5, sticky="se")
        self.reset()
        self.competitions_frame = Competitions(container, self)
        # self.competitions.tkraise()
        # initialize frames
        self.frames = {
            "control": CompetitionControlFrame(container, self),
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
        self.competition = None
        self.user = None

    def change_frame(self, back=False):
        self.frame = self.frames[self.nextframe]
        self.frame.tkraise()
        self.frame.reset(back)
