import tkinter as tk
from tkinter import ttk
from datetime import datetime
import math
import pdfgenerator
from idlelib.tooltip import Hovertip
from shot import Match


class ResultFrame(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        # field options
        options = {"padx": 5, "pady": 0}
        self.i = 0
        self.scalefactor = 1
        self.shotcircles = {}
        self.canvsize = 200
        self.canvas = tk.Canvas(
            self, bg="white", height=self.canvsize, width=self.canvsize
        )
        self.canvas.place(height=self.canvsize, width=self.canvsize)

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
            y=self.canvsize * 0 / 8,
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
            y=self.canvsize * 4 / 8,
            height=self.canvsize * 5 / 10,
            width=self.canvsize * 3 / 4,
        )
        self.shotlabellist = []

        # user input
        self.generate_button = ttk.Button(
            self, text="Drucken / Speichern", command=self.actionSpeichern
        )
        self.generate_button.place(
            x=self.canvsize,
            y=self.canvsize,
            height=self.canvsize / 8,
            width=self.canvsize * 3 / 4,
        )
        Hovertip(
            self.generate_button,
            "Ergebnis speichern\nDas Ergebnis wird gespeichert und ein druckbarer Bericht geöffnet",
        )
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

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
        if self.i == 0 or self.i > len(self.parent.match.series):
            self.i = 0
            self.actuallist = self.parent.match
            self.serieslabel.config(text="Gesammt")
            self.resultlabelframe.config(text="Gesammtergebnis")
            self.redraw_shots()
            self.write_shots()
        else:
            self.actuallist = self.parent.match.series[self.i - 1]
            self.serieslabel.config(text="Serie {:d}".format(self.i))
            self.resultlabelframe.config(text="Serie {:d}".format(self.i))
            self.redraw_shots()
            self.write_shots()

    def actionBack(self):
        self.i -= 1
        if self.i < 0:
            self.i = len(self.parent.match.series)
            self.actuallist = self.parent.match.series[self.i - 1]
            self.serieslabel.config(text="Serie {:d}".format(self.i))
            self.resultlabelframe.config(text="Serie {:d}".format(self.i))
        elif self.i == 0:
            self.i = len(self.parent.match.series)
            self.actuallist = self.parent.match
            self.serieslabel.config(text="Gesammt")
            self.resultlabelframe.config(text="Gesammtergebnis")
        else:
            self.actuallist = self.parent.match.series[self.i - 1]
            self.serieslabel.config(text="Serie {:d}".format(self.i))
            self.resultlabelframe.config(text="Serie {:d}".format(self.i))
        self.redraw_shots()
        self.write_shots()

    def actionSpeichern(self):
        if self.parent.userconfig.has_option(self.parent.usersection, "niceness"):
            niceness = (
                self.parent.userconfig.getint(self.parent.usersection, "niceness") + 1
            )
        else:
            niceness = 1
        self.parent.userconfig[self.parent.usersection]["niceness"] = str(niceness)
        with open(self.parent.userconfigpath, "w") as configfile:
            self.parent.userconfig.write(configfile)
        # self.parent.progress.start()
        self.actionCSV()
        self.actionPDF()
        # self.parent.progress.stop()

    def actionCSV(self):
        filedate = datetime.strptime(self.parent.match.datum, "%d.%m.%Y")
        if self.parent.usersection == "Neu":
            filepath = ""
            filename = (
                datetime.strftime(filedate, "%y%m%d")
                + "_"
                + self.parent.match.name.replace(" ", "_")
            )

        else:
            filepath = self.parent.match.name.replace(" ", "_") + "\\csv"
            filename = datetime.strftime(filedate, "%y%m%d")

        pdfgenerator.CSVgen.makeCSV(self.parent.match, filepath, filename)
        # self.csv_button['state']='disabled'

    def actionPDF(self):
        filedate = datetime.strptime(self.parent.match.datum, "%d.%m.%Y")
        if self.parent.usersection == "Neu":
            filepath = ""
            filename = f"""{datetime.strftime(filedate, "%y%m%d")}_{self.parent.match.scheibentyp}_{self.parent.match.name.replace(" ", "_")}"""
        else:
            filepath = self.parent.match.name.replace(" ", "_")
            filename = f"""{datetime.strftime(filedate, "%y%m%d")}_{self.parent.match.scheibentyp}"""

        pdfgenerator.PDFgen.makePDF(
            self.parent.match, filepath, filename, self.parent.is_extended
        )
        self.generate_button["state"] = "disabled"

    """def recalc(self,event=None):
        self.parent.match.getOutliers(l=self.l_value.get())
        self.redraw_shots()"""

    def redraw_shots(self):
        self.shotcircles.clear()
        self.canvas.delete("shot")
        radiusTen = Match.radius_dict[self.parent.match.scheibentyp][0]
        radiusInnerTen = Match.radius_dict[self.parent.match.scheibentyp][1]
        incrementRing = Match.radius_dict[self.parent.match.scheibentyp][2]
        radiusBlack = Match.radius_dict[self.parent.match.scheibentyp][3]
        radiusCalibre = Match.radius_dict[self.parent.match.scheibentyp][4]
        # self.canvas.xview_moveto(self.origX)
        # self.canvas.yview_moveto(self.origY)
        for a in self.actuallist:
            id = self.canvas.create_oval(
                (a.x - radiusCalibre) * self.scalefactor + self.canvsize / 2,
                -(a.y - radiusCalibre) * self.scalefactor + self.canvsize / 2,
                (a.x + radiusCalibre) * self.scalefactor + self.canvsize / 2,
                -(a.y + radiusCalibre) * self.scalefactor + self.canvsize / 2,
                # fill="orange" if a in self.parent.match.ausreisser else "green",
                fill="green",
                tag="shot",
                activefill="cyan",
            )
            self.shotcircles[id] = a
            self.canvas.tag_bind(id, "<Enter>", self.update_text)

    def update_text(self, event):
        id = self.canvas.find_withtag("current")[0]
        self.ringlabel.config(
            text=(
                "{:.1f}".format(self.shotcircles[id].ringe)
                if self.parent.match.zehntel
                else "{:d}".format(math.floor(self.shotcircles[id].ringe))
            )
        )
        self.xlabel.config(text="{:.2f}".format(self.shotcircles[id].x / 100))

        self.ylabel.config(text="{:.2f}".format(self.shotcircles[id].y / 100))

        self.teilerlabel.config(text="{:.1f}".format(self.shotcircles[id].teiler / 10))

    def redraw_target(self):
        self.canvas.delete("ring")
        radiusTen = Match.radius_dict[self.parent.match.scheibentyp][0]
        radiusInnerTen = Match.radius_dict[self.parent.match.scheibentyp][1]
        incrementRing = Match.radius_dict[self.parent.match.scheibentyp][2]
        radiusBlack = Match.radius_dict[self.parent.match.scheibentyp][3]
        radiusCalibre = Match.radius_dict[self.parent.match.scheibentyp][4]
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

    def write_shots(self):
        self.resultlabel.config(
            text=(
                "{:.1f}".format(self.actuallist.summe)
                if self.actuallist.zehntel
                else "{:d}".format(self.actuallist.summe_ganz)
            )
        )
        self.schnittlabel.config(
            text=(
                "{:.2f}".format(self.actuallist.summe / self.actuallist.anzahl)
                if self.actuallist.zehntel
                else "{:.2f}".format(
                    self.actuallist.summe_ganz / self.actuallist.anzahl
                )
            )
        )
        self.devxlabel.config(text="{:.1f}".format(self.actuallist.ablageRL / 100))
        self.devylabel.config(text="{:.1f}".format(self.actuallist.ablageHT / 100))
        for label in self.shotlabellist:
            label.destroy()
        self.shotlabellist = []
        for n, A in enumerate(self.actuallist):
            label = ttk.Label(
                self,
                text=(
                    "{:.1f}".format(A.ringe)
                    if self.parent.match.zehntel
                    else "{:d}".format(math.floor(A.ringe))
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
        if isinstance(self.actuallist, Match):
            for n, S in enumerate(self.actuallist.series):
                label = ttk.Label(
                    self,
                    text=(
                        "{:.1f}".format(S.summe)
                        if self.parent.match.zehntel
                        else "{:d}".format(S.summe_ganz)
                    ),
                    anchor="center",
                )
                label.place(
                    x=(15 / 8 + n / 6) * self.canvsize,
                    y=(11 / 11) * self.canvsize,
                    height=self.canvsize / 11,
                    width=self.canvsize / 6,
                )
                self.shotlabellist.append(label)
        else:
            label = ttk.Label(
                self,
                text=(
                    "{:.1f}".format(self.actuallist.summe)
                    if self.parent.match.zehntel
                    else "{:d}".format(self.actuallist.summe_ganz)
                ),
                anchor="center",
            )
            label.place(
                x=(15 / 8) * self.canvsize,
                y=self.canvsize,
                height=self.canvsize / 11,
                width=self.canvsize / 6,
            )
            self.shotlabellist.append(label)

    def reset(self, back=False):
        self.generate_button["state"] = "normal"

        self.actuallist = self.parent.match
        self.write_shots()

        # self.l_slider.set(1)
        self.redraw_target()
        self.redraw_shots()
