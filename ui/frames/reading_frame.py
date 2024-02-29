import datetime
import tkinter as tk
import time
from tkinter import messagebox
from tkinter import ttk
from data.match import RADIUS_DICT, Match
from machines.machine import MachineException, ReadingNotAvailable, ReadingThread
from .default_frame import DefaultFrame


class ReadingFrame(DefaultFrame):
    def __init__(self, container, parent):
        super().__init__(container, parent)
        self.reader: ReadingThread = None
        self.stopped = False
        # field options
        options = {"padx": 5, "pady": 0}
        self.statusbox = tk.Listbox(self, state="normal")
        self.statusbox.grid(column=0, row=0, sticky="nesw")

        self.canvsize = 200
        self.canvas = tk.Canvas(
            self, bg="white", height=self.canvsize, width=self.canvsize
        )
        self.canvas.grid(column=1, row=0, sticky="nse")
        self.stopbutton = ttk.Button(self, text="Stop", command=self.stop_reading)
        self.stopbutton.grid(column=1, row=1, padx=5, pady=5, sticky="nse")

        self.columnconfigure(0, weight=1)
        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

    def stop_reading(self):
        if self.reader:
            self.reader.shutdown = True
        self.stopped = True

    def actionStart(self):
        machine = self.source
        self.statusbox.insert("end", "Port wird geöffnet...")
        self.container.update()
        self.statusbox.insert("end", "Einstellungen werden übergeben...")
        self.container.update()
        try:
            if self.current_match:
                self.type_of_target = self.current_match.type_of_target
                self.redraw_target()
                for shot in self.current_match.shots:
                    self.draw_shot(shot)

                machine.config(rest=self.competition.count - self.current_match.anzahl)
            else:
                machine.config()  # config for the rest of series or default
            config_success = True
        except MachineException as e:
            self.statusbox.insert("end", e.message)
            self.container.update()
            self.activate_back_button()
            config_success = False
        if config_success:
            self.statusbox.insert("end", "Scheiben eingeben!")
            self.container.update()
            self.reader = machine.get_reading_thread()
            self.reader.start()
            first = True if not self.current_match else False
            while not self.reader.is_finished():
                self.container.update()
                try:
                    shot, type_of_target = self.reader.get_reading()
                except ReadingNotAvailable:
                    time.sleep(0.5)
                    continue
                if not type_of_target == self.competition.type_of_target:
                    self.reader.shutdown = True
                    self.statusbox.insert("end", "Falscher Scheibentyp")
                    self.container.update()
                    messagebox.showerror("Falscher Scheibentyp", "Falscher Scheibentyp")
                    self.recede()
                    return
                self.type_of_target = type_of_target
                if first:
                    first = False
                    self.redraw_target()
                self.draw_shot(shot)
            if self.reader.shutdown and not self.stopped:
                return
            if len(self.reader.get_result()) == 0:
                self.recede()
                return
            self.stopped = False
            self.statusbox.insert("end", "Einlesen abgeschlossen")
            self.container.update()
            if not self.current_match:
                self.current_match = Match(
                    date=datetime.date.today().strftime("%d.%m.%Y"),
                    shooter=self.user.id,
                    type_of_target=self.type_of_target,
                    shots=self.reader.get_result(),
                    club=self.club.id if self.club else "",
                    team=self.team.id if self.team else "",
                )
                self.matches.add_match(self.current_match)
                self.user.add_match(self.current_match)
                if self.add_to_current_competition:
                    self.user.niceness += 1
                    self.user.add_competition(self.competition)
                    self.current_match.add_competition(self.competition)
                    self.competition.add_match(self.current_match)
                self.users.save()
            else:
                self.current_match.shots.extend(self.reader.get_result())
            if len(self.current_match.shots) >= self.competition.count:
                self.current_match.active = False
            else:
                self.current_match.active = True
            self.matches.save()
            self.competitions.save()
        else:
            return

        self.activate_back_button()
        self.activate_ok_button()
        self.proceed()

    def draw_shot(self, shot):
        radiusCalibre = RADIUS_DICT[self.type_of_target][4]
        self.canvas.create_oval(
            (shot.x * 100 - radiusCalibre) * self.scalefactor + self.canvsize / 2,
            -(shot.y * 100 - radiusCalibre) * self.scalefactor + self.canvsize / 2,
            (shot.x * 100 + radiusCalibre) * self.scalefactor + self.canvsize / 2,
            -(shot.y * 100 + radiusCalibre) * self.scalefactor + self.canvsize / 2,
            # fill="orange" if a in self.match.ausreisser else "green",
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
        self.canvas.create_oval(
            (-radiusBlack) * self.scalefactor + self.canvsize / 2,
            radiusBlack * self.scalefactor + self.canvsize / 2,
            radiusBlack * self.scalefactor + self.canvsize / 2,
            -radiusBlack * self.scalefactor + self.canvsize / 2,
            fill="black",
            tag="ring",
        )

        self.ringcircles = [
            self.canvas.create_oval(
                -(i * incrementRing + radiusTen) * self.scalefactor + self.canvsize / 2,
                (i * incrementRing + radiusTen) * self.scalefactor + self.canvsize / 2,
                (i * incrementRing + radiusTen) * self.scalefactor + self.canvsize / 2,
                -(i * incrementRing + radiusTen) * self.scalefactor + self.canvsize / 2,
                outline="white" if i * incrementRing < radiusBlack else "black",
                tag="ring",
            )
            for i in range(10)
        ]

    def clear_target(self):
        self.canvas.delete("ring")
        self.canvas.delete("shot")

    def reset(self):
        self.clear_target()
        self.activate_back_button()
        self.deactivate_ok_button()
        self.statusbox.delete("0", "end")
        self.statusbox.insert("end", "Bereit zum Einlesen")
        self.actionStart()
