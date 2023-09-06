import os
from threading import Thread
import time
from tkinter import *
from tkinter.ttk import *
from typing import TYPE_CHECKING

from data.competition import Competition
from data.match import RADIUS_DICT, Match

if TYPE_CHECKING:
    from ui.frames.control_frame import ControlFrame


class Visualisation(Toplevel):
    def __init__(self, master: "ControlFrame" = None):
        super().__init__(master=master)
        self.parent = master
        self.title("Visualisierung")
        self.geometry("800x800")
        self.iconbitmap(os.path.join("ui", "logo.ico"))
        self.competition_frames = {}

        self.keep_updating = False

    def show_competitions(self):
        for competition in self.parent.active_competitions:
            self.competition_frames[competition.id] = VisualisationFrame(
                self, competition
            )
        self.competition_frames[competition.id].tkraise()
        self.keep_updating = True
        self.update_thread = Thread(target=self.update_thread_function).start()

    def update_thread_function(self):
        while self.keep_updating:
            for id in self.competition_frames:
                self.competition_frames[id].tkraise()
                time.sleep(2)


class VisualisationFrame(Frame):
    def __init__(self, container, competition: Competition):
        super().__init__(container)
        self.container = container
        self.width = self.container.winfo_width() - 20
        self.height = self.container.winfo_height() - 20
        self.count = len(competition.entries)
        self.size = min(self.height / 2, 2 * self.width / self.count)
        self.match_frames = {}
        label = Label(self, text=competition.name)
        label.grid(column=0, row=0)
        for i, entry_id in enumerate(competition.entries):
            self.match_frames[entry_id] = ResultFrame(
                self, self.container.parent.matches[entry_id]
            )
            self.match_frames[entry_id].grid(
                row=i % 2 + 1, column=i // 2, sticky="nesw"
            )
        self.grid(row=0, column=0, sticky="nesw")


class ResultFrame(Frame):
    def __init__(self, container, match: Match):
        self.container = container
        super().__init__(container)
        label = Label(self, text=match.shooter.name)
        label.grid(column=0, row=0)
        self.match = match

        self.canvas = Canvas(
            self, bg="white", height=self.container.size, width=self.container.size
        )
        self.canvas.grid(row=1, column=0)
        self.draw_target()
        self.redraw_shots()

    def draw_target(self):
        self.canvas.delete("ring")
        radiusTen = RADIUS_DICT[self.match.type_of_target][0]
        incrementRing = RADIUS_DICT[self.match.type_of_target][2]
        radiusBlack = RADIUS_DICT[self.match.type_of_target][3]
        w = 2 * (radiusTen + 9 * incrementRing)
        scalefactor = self.container.size / w
        spiegel = self.canvas.create_oval(
            (-radiusBlack) * scalefactor + self.container.size / 2,
            radiusBlack * scalefactor + self.container.size / 2,
            radiusBlack * scalefactor + self.container.size / 2,
            -radiusBlack * scalefactor + self.container.size / 2,
            fill="black",
            tag="ring",
        )

        self.ringcircles = [
            self.canvas.create_oval(
                (-i * incrementRing) * scalefactor + self.container.size / 2,
                -(-i * incrementRing) * scalefactor + self.container.size / 2,
                (i * incrementRing) * scalefactor + self.container.size / 2,
                -(i * incrementRing) * scalefactor + self.container.size / 2,
                outline="white" if i * incrementRing < radiusBlack else "black",
                tag="ring",
            )
            for i in range(1, 10)
        ]

    def redraw_shots(self):
        self.canvas.delete("shot")
        radiusCalibre = RADIUS_DICT[self.match.type_of_target][4]
        radiusTen = RADIUS_DICT[self.match.type_of_target][0]
        incrementRing = RADIUS_DICT[self.match.type_of_target][2]
        # self.canvas.xview_moveto(self.origX)
        # self.canvas.yview_moveto(self.origY)
        w = 2 * (radiusTen + 9 * incrementRing)
        scalefactor = self.container.size / w
        for shot in self.match.shots:
            id = self.canvas.create_oval(
                (shot.x - radiusCalibre) * scalefactor + self.container.size / 2,
                -(shot.y - radiusCalibre) * scalefactor + self.container.size / 2,
                (shot.x + radiusCalibre) * scalefactor + self.container.size / 2,
                -(shot.y + radiusCalibre) * scalefactor + self.container.size / 2,
                # fill="orange" if a in self.match.ausreisser else "green",
                fill="green",
                tag="shot",
                activefill="cyan",
            )
