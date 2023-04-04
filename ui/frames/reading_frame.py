import tkinter as tk
from tkinter import ttk
import time
from data.match import RADIUS_DICT
from machines.machine import MachineException


class ReadingFrame(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        self.container = container

        # field options
        options = {"padx": 5, "pady": 0}
        self.statusbox = tk.Listbox(self, state="normal")
        self.statusbox.grid(column=0, row=0, sticky="nesw")

        self.canvsize = 200
        self.canvas = tk.Canvas(
            self, bg="white", height=self.canvsize, width=self.canvsize
        )
        self.canvas.grid(column=1, row=0, sticky="nse")

        self.columnconfigure(0, weight=1)
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def actionStart(self):
        machine = self.parent.competition.source
        self.statusbox.insert("end", "Port wird geöffnet...")
        self.container.update()
        self.statusbox.insert("end", "Einstellungen werden übergeben...")
        self.container.update()
        try:
            machine.config()
            config_success = True
        except MachineException as e:
            self.statusbox.insert("end", e.message)
            self.container.update()
            self.parent.back_button["state"] = "normal"
            config_success = False
        if config_success:
            self.statusbox.insert("end", "Scheiben eingeben!")
            self.container.update()
            reader = machine.get_reading_thread()
            reader.start()
            first = True
            while not reader.is_finished():
                shot, self.type_of_target = reader.get_reading()
                if shot == None:
                    time.sleep(0.5)
                else:
                    if first:
                        first = False
                        self.redraw_target()
                    self.draw_shot(shot)
                    self.container.update()
            self.statusbox.insert("end", "Einlesen abgeschlossen")
            self.container.update()
            self.parent.competition.current_match.fromShotlist(reader.get_result())
        else:
            return

        self.parent.back_button["state"] = "normal"
        self.parent.ok_button["state"] = "normal"
        # self.parent.progress.stop()
        self.parent.actionOK()

    def draw_shot(self, shot):
        radiusCalibre = RADIUS_DICT[self.type_of_target][4]
        self.canvas.create_oval(
            (shot.x - radiusCalibre) * self.scalefactor + self.canvsize / 2,
            -(shot.y - radiusCalibre) * self.scalefactor + self.canvsize / 2,
            (shot.x + radiusCalibre) * self.scalefactor + self.canvsize / 2,
            -(shot.y + radiusCalibre) * self.scalefactor + self.canvsize / 2,
            # fill="orange" if a in self.parent.match.ausreisser else "green",
            fill="green",
            tag="shot",
            activefill="cyan",
        )

    def redraw_target(self):
        self.clear_target()
        radiusTen = RADIUS_DICT[self.type_of_target][0]
        incrementRing = RADIUS_DICT[self.type_of_target][2]
        radiusBlack = RADIUS_DICT[self.type_of_target][3]
        w = 2 * (radiusTen + 9 * incrementRing)
        self.scalefactor = self.canvsize / w
        spiegel = self.canvas.create_oval(
            (-radiusBlack) * self.scalefactor + self.canvsize / 2,
            radiusBlack * self.scalefactor + self.canvsize / 2,
            radiusBlack * self.scalefactor + self.canvsize / 2,
            -radiusBlack * self.scalefactor + self.canvsize / 2,
            fill="black",
            tag="ring",
        )

        self.ringcircles = [
            self.canvas.create_oval(
                (-i * incrementRing) * self.scalefactor + self.canvsize / 2,
                -(-i * incrementRing) * self.scalefactor + self.canvsize / 2,
                (i * incrementRing) * self.scalefactor + self.canvsize / 2,
                -(i * incrementRing) * self.scalefactor + self.canvsize / 2,
                outline="white" if i * incrementRing < radiusBlack else "black",
                tag="ring",
            )
            for i in range(1, 10)
        ]

    def clear_target(self):
        self.canvas.delete("ring")
        self.canvas.delete("shot")

    def reset(self, back=False):
        self.clear_target()
        self.parent.back_button["state"] = "normal"
        self.parent.ok_button["state"] = "disabled"
        # self.start_button["state"] = "normal"
        self.statusbox.delete("0", "end")
        self.statusbox.insert("end", "Bereit zum Einlesen")
        self.actionStart()
