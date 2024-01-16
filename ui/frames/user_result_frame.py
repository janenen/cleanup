import tkinter as tk
from tkinter import ttk
from data.series import Series
import ui.frames.output_frame as output_frame
from idlelib.tooltip import Hovertip
from data.match import RADIUS_DICT
from .default_frame import DefaultFrame


class UserResultFrame(DefaultFrame):
    actuallist: Series

    def __init__(self, container, parent):
        super().__init__(container, parent)
        # field options
        options = {"padx": 5, "pady": 0}
        self.i = 0
        self.shotcircles = {}
        self.canvsize = 220
        self.canvas = tk.Canvas(
            self, bg="white", height=self.canvsize, width=self.canvsize
        )
        self.canvas.place(height=self.canvsize, width=self.canvsize)
        self.export = False

        # self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        # self.canvas.bind("<B1-Motion>", self.scroll_move)
        # self.canvas.bind("<MouseWheel>",self.zoomer)
        # self.origX = self.canvas.xview()[0]
        # self.origY = self.canvas.yview()[0]

        self.backbutton = ttk.Button(self, text="<", command=self.actionBack)
        self.backbutton.place(
            x=0, y=self.canvsize, height=self.canvsize / 8, width=self.canvsize / 4
        )
        Hovertip(self.backbutton, "Zu vorheriger Serie / Gesammtdarstellung wechseln")
        self.serieslabel = ttk.Label(self, text="Gesammt", anchor="center")
        self.serieslabel.place(
            x=self.canvsize / 4,
            y=self.canvsize,
            height=self.canvsize / 8,
            width=self.canvsize * 2 / 4,
        )
        self.forebutton = ttk.Button(self, text=">", command=self.actionFore)
        self.forebutton.place(
            x=self.canvsize * 3 / 4,
            y=self.canvsize,
            height=self.canvsize / 8,
            width=self.canvsize / 4,
        )
        Hovertip(self.forebutton, "Zu nächster Serie / Gesammtdarstellung wechseln")

        """ttk.Label(self, text="Ausreissergrenze:").place(x=self.canvsize,y=0,height=self.canvsize/8,width=self.canvsize*3/4)
        self.l_value = tk.DoubleVar()
        self.l_slider = ttk.Scale(self, from_=0, to=1, orient=tk.HORIZONTAL,variable=self.l_value,command=self.recalc)
        self.l_slider.place(x=self.canvsize,y=self.canvsize/8,height=self.canvsize/8,width=self.canvsize*3/4)"""
        self.resultlabelframe = ttk.LabelFrame(self, text="Gesamtergebnis")
        ttk.Label(self.resultlabelframe, text="Ergebnis: ").grid(
            row=0, column=0, sticky="e"
        )
        self.resultlabel = ttk.Label(self.resultlabelframe, text="-")
        self.resultlabel.grid(row=0, column=1, sticky="w")
        ttk.Label(self.resultlabelframe, text="Schnitt: ").grid(
            row=1, column=0, sticky="e"
        )
        self.schnittlabel = ttk.Label(self.resultlabelframe, text="-")
        self.schnittlabel.grid(row=1, column=1, sticky="w")
        ttk.Label(self.resultlabelframe, text="Ablage R/L: ").grid(
            row=2, column=0, sticky="e"
        )
        self.devxlabel = ttk.Label(self.resultlabelframe, text="-")
        self.devxlabel.grid(row=2, column=1, sticky="w")
        ttk.Label(self.resultlabelframe, text="Ablage H/T: ").grid(
            row=3, column=0, sticky="e"
        )
        self.devylabel = ttk.Label(self.resultlabelframe, text="-")
        self.devylabel.grid(row=3, column=1, sticky="w")
        self.resultlabelframe.place(
            x=self.canvsize,
            y=self.canvsize * 0 / 9,
            height=self.canvsize * 5 / 10,
            width=self.canvsize * 3 / 4,
        )

        self.infolabelframe = ttk.LabelFrame(self, text="Schusswert")
        ttk.Label(self.infolabelframe, text="Ringe: ").grid(
            column=0, row=0, sticky="e", **options
        )
        self.ringlabel = ttk.Label(self.infolabelframe, text="-")
        self.ringlabel.grid(column=1, row=0, sticky="w")
        ttk.Label(self.infolabelframe, text="X: ").grid(
            column=0, row=1, sticky="e", **options
        )
        self.xlabel = ttk.Label(self.infolabelframe, text="-")
        self.xlabel.grid(column=1, row=1, sticky="w")
        ttk.Label(self.infolabelframe, text="Y: ").grid(
            column=0, row=2, sticky="e", **options
        )
        self.ylabel = ttk.Label(self.infolabelframe, text="-")
        self.ylabel.grid(column=1, row=2, sticky="w")
        ttk.Label(self.infolabelframe, text="Teiler: ").grid(
            column=0, row=3, sticky="e", **options
        )
        self.teilerlabel = ttk.Label(self.infolabelframe, text="-")
        self.teilerlabel.grid(column=1, row=3, sticky="w")
        self.infolabelframe.place(
            x=self.canvsize,
            y=self.canvsize * 4 / 9,
            height=self.canvsize * 5 / 10,
            width=self.canvsize * 3 / 4,
        )
        self.shotlabellist = []

        self.inputlabelframe = ttk.LabelFrame(self, text="Speichern")
        # user input
        self.generate_button = ttk.Button(
            self.inputlabelframe,
            text="Exportieren",
            command=self.action_export,
        )
        self.generate_button.grid(column=0, row=0, sticky="we")
        self.inputlabelframe.place(
            x=self.canvsize,
            y=self.canvsize * 8 / 9,
            height=self.canvsize * 3 / 9,
            width=self.canvsize * 3 / 4,
        )
        Hovertip(
            self.generate_button,
            "Ergebnis speichern\nDas Ergebnis wird gespeichert und ein druckbarer Bericht geöffnet",
        )
        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

    """def scroll_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
    def zoomer(self,event):
        if (event.delta > 0):
            self.canvas.scale("all", self.canvas.canvasx(event.x), self.canvas.canvasy(event.y), 1.1, 1.1)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))"""

    def actionFore(self):
        self.i += 1
        if self.i == 0 or self.i > len(self.current_match.shots) / 10:
            self.i = 0
            self.actuallist = Series(self.current_match.shots)
            self.serieslabel.config(text="Gesammt")
            self.resultlabelframe.config(text="Gesammtergebnis")
            self.redraw_shots()
            self.write_shots()
        else:
            start_index = (self.i - 1) * 10
            end_index = start_index + 10
            self.actuallist = Series(self.current_match.shots[start_index:end_index])
            self.serieslabel.config(text=f"Serie {self.i}")
            self.resultlabelframe.config(text=f"Serie {self.i}")
            self.redraw_shots()
            self.write_shots()

    def actionBack(self):
        self.i -= 1
        if self.i < 0:
            self.i = len(self.current_match.shots) // 10 + 1
            start_index = (self.i - 1) * 10
            end_index = start_index + 10
            self.actuallist = Series(self.current_match.shots[start_index:end_index])
            self.serieslabel.config(text=f"Serie {self.i}")
            self.resultlabelframe.config(text=f"Serie {self.i}")
        elif self.i == 0:
            self.actuallist = Series(self.current_match.shots)
            self.serieslabel.config(text="Gesammt")
            self.resultlabelframe.config(text="Gesammtergebnis")
        else:
            start_index = (self.i - 1) * 10
            end_index = start_index + 10
            self.actuallist = Series(self.current_match.shots[start_index:end_index])
            self.serieslabel.config(text=f"Serie {self.i}")
            self.resultlabelframe.config(text=f"Serie {self.i}")
        self.redraw_shots()
        self.write_shots()

    def action_export(self):
        self.export = True
        self.proceed()

    """def recalc(self,event=None):
        self.current_match.getOutliers(l=self.l_value.get())
        self.redraw_shots()"""

    def redraw_shots(self):
        self.shotcircles.clear()
        self.canvas.delete("shot")
        radiusCalibre = RADIUS_DICT[self.current_match.type_of_target][4]
        radiusTen = RADIUS_DICT[self.current_match.type_of_target][0]
        incrementRing = RADIUS_DICT[self.current_match.type_of_target][2]
        # self.canvas.xview_moveto(self.origX)
        # self.canvas.yview_moveto(self.origY)
        w = 2 * (radiusTen + 9 * incrementRing)
        scalefactor = self.canvsize / w
        for shot in self.actuallist:
            id = self.canvas.create_oval(
                (shot.x * 100 - radiusCalibre) * scalefactor + self.canvsize / 2,
                -(shot.y * 100 - radiusCalibre) * scalefactor + self.canvsize / 2,
                (shot.x * 100 + radiusCalibre) * scalefactor + self.canvsize / 2,
                -(shot.y * 100 + radiusCalibre) * scalefactor + self.canvsize / 2,
                # fill="orange" if a in self.current_match.ausreisser else "green",
                fill="green",
                tag="shot",
                activefill="cyan",
            )
            self.shotcircles[id] = shot
            self.canvas.tag_bind(id, "<Enter>", self.update_text)

    def update_text(self, event):
        id = self.canvas.find_withtag("current")[0]
        self.ringlabel.config(
            text=(
                "{:.1f}".format(self.shotcircles[id].ringe)
                if self.competition.decimal
                else f"{self.shotcircles[id].ringe_ganz}"
            )
        )
        self.xlabel.config(text="{:.2f}".format(self.shotcircles[id].x))

        self.ylabel.config(text="{:.2f}".format(self.shotcircles[id].y))

        self.teilerlabel.config(text="{:.1f}".format(self.shotcircles[id].teiler))

    def redraw_target(self):
        self.canvas.delete("ring")
        radiusTen = RADIUS_DICT[self.current_match.type_of_target][0]
        incrementRing = RADIUS_DICT[self.current_match.type_of_target][2]
        radiusBlack = RADIUS_DICT[self.current_match.type_of_target][3]
        w = 2 * (radiusTen + 9 * incrementRing)
        scalefactor = self.canvsize / w
        spiegel = self.canvas.create_oval(
            (-radiusBlack) * scalefactor + self.canvsize / 2,
            radiusBlack * scalefactor + self.canvsize / 2,
            radiusBlack * scalefactor + self.canvsize / 2,
            -radiusBlack * scalefactor + self.canvsize / 2,
            fill="black",
            tag="ring",
        )

        self.ringcircles = [
            self.canvas.create_oval(
                (-i * incrementRing) * scalefactor + self.canvsize / 2,
                -(-i * incrementRing) * scalefactor + self.canvsize / 2,
                (i * incrementRing) * scalefactor + self.canvsize / 2,
                -(i * incrementRing) * scalefactor + self.canvsize / 2,
                outline="white" if i * incrementRing < radiusBlack else "black",
                tag="ring",
            )
            for i in range(1, 10)
        ]

    def write_shots(self):
        self.resultlabel.config(
            text=(
                "{:.1f}".format(self.actuallist.summe)
                if self.competition.decimal
                else "{:d}".format(self.actuallist.summe_ganz)
            )
        )
        self.schnittlabel.config(
            text=(
                "{:.2f}".format(self.actuallist.summe / self.actuallist.anzahl)
                if self.competition.decimal
                else "{:.2f}".format(
                    self.actuallist.summe_ganz / self.actuallist.anzahl
                )
            )
        )
        self.devxlabel.config(text="{:.1f}".format(self.actuallist.ablageRL))
        self.devylabel.config(text="{:.1f}".format(self.actuallist.ablageHT))
        for label in self.shotlabellist:
            label.destroy()
        self.shotlabellist = []
        for n, shot in enumerate(self.current_match.shots):
            label = ttk.Label(
                self,
                text=(
                    "{:.1f}".format(shot.ringe)
                    if self.competition.decimal
                    else "{:d}".format(shot.ringe_ganz)
                ),
                anchor="center",
            )
            label.place(
                x=(15 / 8 + int(n / 10) / 6) * self.canvsize,
                y=((n % 10) / 11) * self.canvsize,
                height=self.canvsize / 11,
                width=self.canvsize / 6,
            )
            self.shotlabellist.append(label)
            if n > 0 and (n + 1) % 10 == 0:
                end_index = n + 1
                start_index = end_index - 10
                current_series = Series(self.current_match.shots[start_index:end_index])
                label = ttk.Label(
                    self,
                    text=(
                        "{:.1f}".format(current_series.summe)
                        if self.competition.decimal
                        else "{:d}".format(current_series.summe_ganz)
                    ),
                    anchor="center",
                )
                label.place(
                    x=(15 / 8 + (n // 10) / 6) * self.canvsize,
                    y=(11 / 11) * self.canvsize,
                    height=self.canvsize / 11,
                    width=self.canvsize / 6,
                )
                self.shotlabellist.append(label)

    def reset(self):
        self.activate_ok_button()
        self.deactivate_back_button()

        self.actuallist = Series(self.current_match.shots)
        self.parent.competitions_frame.competition_listbox.configure(state="normal")
        self.parent.competitions_frame.update_entries()
        self.serieslabel.config(text="Gesammt")
        self.resultlabelframe.config(text="Gesammtergebnis")
        self.write_shots()

        # self.l_slider.set(1)
        self.redraw_target()
        self.redraw_shots()
