from math import ceil
import os
import sys
from threading import Thread
import time
import tkinter as tk
import tkinter.ttk as ttk
from typing import TYPE_CHECKING

from data.competition import Competition
from data.match import RADIUS_DICT, Match

if TYPE_CHECKING:
    from ui.frames.control_frame import ControlFrame


class Visualisation(tk.Toplevel):
    def __init__(self, master: "ControlFrame" = None):
        super().__init__(master=master)
        self.parent = master
        self.title("Visualisierung")
        self.geometry("1130x800")
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        self.iconbitmap(os.path.join(base_path, "ui", "logo.ico"))
        self.competition_frames: dict[str, CompetitionVisualisationFrame] = {}
        self.keep_updating = True
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        Thread(target=self.update_thread_function).start()

    def update_frame(self):
        for competition in self.parent.active_competitions:
            if competition.entries:
                if not competition.id in self.competition_frames.keys():
                    self.competition_frames[competition.id] = (
                        CompetitionVisualisationFrame(self, competition)
                    )
            for frame in self.competition_frames.keys():
                if frame not in [comp.id for comp in self.parent.active_competitions]:
                    del self.competition_frames[frame]

    def update_thread_function(self):
        while self.keep_updating:
            self.update_frame()
            try:
                for id in self.competition_frames:
                    self.competition_frames[id].update_frame()
                    self.competition_frames[id].tkraise()
                    time.sleep(2)
            except tk.TclError as e:
                print(e)
                self.keep_updating = False


class CompetitionVisualisationFrame(ttk.Frame):
    def __init__(self, container, competition: Competition):
        super().__init__(container)
        self.container: Visualisation = container
        self.competition: Competition = competition
        self.frame_size = 0

        self.match_frames: dict[str, ResultVisualisationFrame] = {}
        label = ttk.Label(self, text=competition.name)

        label.grid(column=0, row=0)

        self.grid(row=0, column=0, sticky="nesw")

    def update_frame(self):
        c = 20
        combinations = []
        k = len(self.competition.entries)
        for i in range(k):
            combinations.append((i + 1, ceil(k / (i + 1))))
        width = self.winfo_width()
        height = self.winfo_height()
        optimal_combination = (1, 1)
        area = 0
        size = 0
        for combination in combinations:
            max_height = (height - combination[0] * c) / combination[0]
            max_width = (width - 20) / combination[1]
            constrian = min(max_height, max_width)
            area0 = constrian * (constrian + c)
            if area0 > area:
                optimal_combination = combination
                area = area0
                size = constrian
        m = optimal_combination[0]
        n = optimal_combination[1]
        if not size == self.frame_size:
            self.frame_size = size
            for frame in self.match_frames.items():
                frame[1].destroy()
            self.match_frames.clear()

        for match_id in self.competition.entries:  # ToDo Update
            if not match_id in self.match_frames.keys():
                # print("new frame")
                self.match_frames[match_id] = ResultVisualisationFrame(
                    self, self.container.parent.matches[match_id]
                )
            else:
                # print("update")
                self.match_frames[match_id].update_frame()
        for i, frame in enumerate(self.match_frames.items()):
            frame[1].grid(row=i // n, column=i % n, sticky="nesw")


class ResultVisualisationFrame(ttk.Frame):
    def __init__(self, container, match: Match):
        self.container: CompetitionVisualisationFrame = container
        super().__init__(container)
        label = ttk.Label(
            self, text=self.container.container.parent.users[match.shooter].name
        )
        label.grid(column=0, row=0)

        self.match: Match = match

        self.canvas = tk.Canvas(
            self,
            bg="white",
            height=self.container.frame_size,
            width=self.container.frame_size,
        )

        self.canvas.grid(row=1, column=0)
        self.update_frame()
        # print(f"c={label.winfo_height()}")

    def update_frame(self):
        self.draw_target()
        self.redraw_shots()

    def draw_target(self):
        self.canvas.delete("ring")
        radiusTen = RADIUS_DICT[self.match.type_of_target][0]
        incrementRing = RADIUS_DICT[self.match.type_of_target][2]
        radiusBlack = RADIUS_DICT[self.match.type_of_target][3]
        w = 2 * (radiusTen + 9 * incrementRing)
        scalefactor = self.container.frame_size / w
        self.canvas.create_oval(
            (-radiusBlack) * scalefactor + self.container.frame_size / 2,
            radiusBlack * scalefactor + self.container.frame_size / 2,
            radiusBlack * scalefactor + self.container.frame_size / 2,
            -radiusBlack * scalefactor + self.container.frame_size / 2,
            fill="black",
            tag="ring",
        )

        self.ringcircles = [
            self.canvas.create_oval(
                -(i * incrementRing + radiusTen) * scalefactor
                + self.container.frame_size / 2,
                (i * incrementRing + radiusTen) * scalefactor
                + self.container.frame_size / 2,
                (i * incrementRing + radiusTen) * scalefactor
                + self.container.frame_size / 2,
                -(i * incrementRing + radiusTen) * scalefactor
                + self.container.frame_size / 2,
                outline="white" if i * incrementRing < radiusBlack else "black",
                tag="ring",
            )
            for i in range(10)
        ]

    def redraw_shots(self):
        self.canvas.delete("shot")
        radiusCalibre = RADIUS_DICT[self.match.type_of_target][4]
        radiusTen = RADIUS_DICT[self.match.type_of_target][0]
        incrementRing = RADIUS_DICT[self.match.type_of_target][2]
        w = 2 * (radiusTen + 9 * incrementRing)
        scalefactor = self.container.frame_size / w
        for shot in self.match.shots:
            self.canvas.create_oval(
                (shot.x * 100 - radiusCalibre) * scalefactor
                + self.container.frame_size / 2,
                -(shot.y * 100 - radiusCalibre) * scalefactor
                + self.container.frame_size / 2,
                (shot.x * 100 + radiusCalibre) * scalefactor
                + self.container.frame_size / 2,
                -(shot.y * 100 + radiusCalibre) * scalefactor
                + self.container.frame_size / 2,
                fill="green",
                tag="shot",
            )
        shotbox = self.canvas.bbox("shot")
        allbox = self.canvas.bbox("all")
        size = (allbox[2] + 1) - (allbox[0] - 1)
        rect = [shotbox[i] - size // 2 for i in range(len(shotbox))]
        r = max(abs(min(rect)), max(rect))
        scale = (size / 2) / r
        self.canvas.scale("all", size // 2, size // 2, scale, scale)
