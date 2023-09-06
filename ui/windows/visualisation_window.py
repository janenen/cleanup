import os
import time
from tkinter import *
from tkinter.ttk import *
from typing import TYPE_CHECKING

from data.competition import Competition
if TYPE_CHECKING:
    from ui.frames.control_frame import ControlFrame


class Visualisation(Toplevel):
    def __init__(self, master:"ControlFrame"=None):

        super().__init__(master=master)
        self.parent=master
        self.title("Visualisierung")
        self.geometry("800x800")
        self.iconbitmap(os.path.join("ui", "logo.ico"))
        self.frames={}


    def show_competitions(self):
        for competition in self.parent.active_competitions:
            self.frames[competition.id]=VisualisationFrame(self,competition)
        self.frames[competition.id].tkraise()



class VisualisationFrame(Frame):
    def __init__(self, container,competition:Competition):
        super().__init__(container)
        self.container = container
        label=Label(self,text=competition.name)
        label.grid(column=0,row=0)
        self.grid(row=0,column=0)