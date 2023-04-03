import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import configparser
from data.match import Match
from ui.frames.select_file_frame import SelectFileFrame
from ui.frames.select_user_frame import SelectUserFrame
from ui.frames.fsk_frame import FSKFrame
from ui.frames.reading_frame import ReadingFrame
from ui.frames.settings_frame import SettingsFrame
from ui.frames.select_port_frame import SelectPortFrame
from ui.frames.result_frame import ResultFrame
from ui.frames.string_frame import StringFrame
from machines.rika import Rika
from machines.disag import Disag
from machines.csv import CSV
from machines.qsd import QSD
from machines.qr import QR

# from analysis_frame import AnalysisFrame


class ControlFrame(ttk.Frame):
    def actionOK(self):
        back = False
        if self.nextframe == "user":
            self.nextframe = "port"

        elif self.nextframe == "port":
            if type(self.quelle) == Rika or type(self.quelle) == Disag:
                self.nextframe = "settings"
            elif type(self.quelle) == QR:
                self.nextframe = "string"
            elif type(self.quelle) == CSV or type(self.quelle) == QSD:
                self.nextframe = "file"

        elif self.nextframe == "file":
            self.nextframe = "settings"

        elif self.nextframe == "string":
            if self.frames["string"].parse_text():
                self.nextframe = "settings"
            else:
                self.nextframe == "string"

        elif self.nextframe == "settings":
            if self.frames["settings"].parseInput():
                self.nextframe = "reading"
            else:
                self.nextframe = "user"

        elif self.nextframe == "reading":
            if self.fsk:
                self.nextframe = "fsk"
            else:
                self.nextframe = "result"

        elif self.nextframe == "fsk":
            self.nextframe = "result"

        # elif self.nextframe == "result":
        #    self.nextframe = "analysis"
        # elif self.nextframe == "analysis":
        elif self.nextframe == "result":
            if self.fsk:
                MsgBox = tk.messagebox.askquestion(
                    "Programm schließen",
                    "Programm schließen?\nAlles gespeichert?\nFehlschussskasse bezahlt?",
                    icon="error",
                )
            else:
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
        if self.nextframe == "result":
            MsgBox = tk.messagebox.askquestion(
                "Alles gespeichert?",
                "Alles gespeichert?",
                icon="error",
            )
            if MsgBox == "yes":
                self.reset()
                self.nextframe = "user"
            else:
                return
        # elif self.nextframe == "analysis":
        #    self.nextframe = "result"
        elif self.nextframe == "reading":
            # close connection
            self.ser.write(b"\xd0")
            self.ser.read(1)
            self.ser.close()
            self.nextframe = "user"
        else:
            self.nextframe = "user"
        self.change_frame(back=True)

    def __init__(self, container):
        super().__init__(container)
        # self['text'] = 'Options'
        self.container = container

        self.nextframe = "user"
        self.ser = serial.Serial()

        #  buttons
        self.back_button = ttk.Button(self, text="Zurück", command=self.actionBack)
        self.back_button.grid(column=1, row=0, padx=5, pady=5)
        self.ok_button = ttk.Button(self, text="OK", command=self.actionOK)
        self.ok_button.grid(column=2, row=0, padx=5, pady=5)
        self.grid(column=0, row=1, padx=5, pady=5, sticky="se")
        self.reset()

        # initialize frames
        self.frames = {
            "port": SelectPortFrame(container, self),
            "settings": SettingsFrame(container, self),
            "reading": ReadingFrame(container, self),
            "result": ResultFrame(container, self),
            "user": SelectUserFrame(container, self),
            "file": SelectFileFrame(container, self),
            "fsk": FSKFrame(container, self),
            "string": StringFrame(container, self),
            # "analysis": AnalysisFrame(container, self),
        }
        self.change_frame()

    def reset(self):
        self.anzahl = 40
        self.proscheibe = 1
        self.match = Match()
        self.userconfig = configparser.ConfigParser()
        self.usersection = ""
        self.userconfigpath = "./schuetzen.ini"
        self.quelle = "maschine"
        self.inputfile = ""
        self.fsk = False
        self.inputstring = ""

    def change_frame(self, back=False):
        frame = self.frames[self.nextframe]
        frame.tkraise()
        frame.reset(back)
