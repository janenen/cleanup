import tkinter as tk
from tkinter import ttk
import time
import pdfgenerator
from shot import Shot, Match


class ReadingFrame(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        self.container = container

        # field options
        options = {"padx": 5, "pady": 0}
        self.statusbox = tk.Listbox(self, state="normal")
        self.statusbox.grid(column=0, row=0, sticky="nesw")
        # ttk.Label(self, text="Scheiben einlesen!").grid(column=0,row=0,sticky="e",**options)
        # self.start_button = tk.Button(self, text="Start", command=self.actionStart)
        # self.start_button.pack()
        self.canvsize = 200
        self.canvas = tk.Canvas(
            self, bg="white", height=self.canvsize, width=self.canvsize
        )
        self.canvas.grid(column=1, row=0, sticky="nse")
        # self.start_button.grid(columnspan=2,column=1,row=1,sticky='e',**options)
        self.columnconfigure(0, weight=1)
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def actionStart(self):
        # self.start_button["state"] = "disabled"
        # self.parent.progress.start()
        if self.parent.quelle == "maschine":
            self.statusbox.insert("end", "Port wird geöffnet...")
            self.container.update()
            self.parent.ser.open()
            self.parent.ser.read()
            self.parent.ser.write(b"\xd1")  # d1 einzeltreffer
            ans = self.parent.ser.read(3)
            if ans != b"200":
                self.parent.ser.close()
                return

            self.statusbox.insert("end", "Einstellungen werden übergeben...")
            self.container.update()
            # ESC S XXX CR
            self.parent.ser.write(
                b"\x1bS" + bytes(str(self.parent.anzahl).zfill(3), "utf-8") + b"\x0d"
            )
            ans = self.parent.ser.read(1)
            if ans != b"\06":
                self.statusbox.insert("end", "Anzahl konnte nicht übernommen werden")
                self.container.update()
                self.parent.ser.write(b"\xd0")
                self.parent.ser.close()
                self.parent.back_button["state"] = "normal"
                return
            # ESC U X CR
            self.parent.ser.write(
                b"\x1bU"
                + bytes(str(self.parent.proscheibe).zfill(1), "utf-8")
                + b"\x0d"
            )
            ans = self.parent.ser.read(1)
            if ans != b"\06":
                self.statusbox.insert(
                    "end", "Schuss/Scheibe konnte nicht übernommen werden"
                )
                self.parent.ser.write(b"\xd0")
                self.parent.ser.close()
                self.parent.back_button["state"] = "normal"
                return
            # ESC Z 3 CR
            self.parent.ser.write(b"\x1bZ3\x0d")
            ans = self.parent.ser.read(1)
            if ans != b"\06":
                self.statusbox.insert(
                    "end", "Teilerwertung konnte nicht übernommen werden"
                )
                self.parent.ser.write(b"\xd0")
                self.parent.ser.close()
                self.parent.back_button["state"] = "normal"
                return
            self.statusbox.insert("end", "Scheiben eingeben!")
            self.container.update()
            first = True
            while len(self.parent.shotlist) < self.parent.anzahl:
                self.container.update()
                self.parent.ser.write(b"\x16")
                ans = self.parent.ser.read(1)

                if ans == b"\x01":

                    ans = self.parent.ser.read(32 + 24 + 2)
                    self.parent.match.scheibentyp = (
                        str(ans[22:24]).replace("b", "").replace("'", "")
                    )
                    if first:
                        self.redraw_target()
                        first = False
                    self.parent.shotlist.append(
                        Shot(
                            ringe=int(ans[32 : 32 + 3]) / 10,
                            teiler=int(ans[32 + 4 : 32 + 9]),
                            x=int(ans[32 + 10 : 32 + 16]),
                            y=int(ans[32 + 17 : 32 + 23]),
                        )
                    )
                    self.parent.ser.write(b"\x0c")  # FF
                    self.draw_shot(self.parent.shotlist[-1])
                    self.container.update()
                else:
                    time.sleep(0.5)
            self.statusbox.insert("end", "Einlesen abgeschlossen")
            self.parent.ser.write(b"\xd0")
            self.parent.ser.read(1)
            self.parent.ser.close()

            self.parent.match.fromShotlist(self.parent.shotlist)
        else:
            self.statusbox.insert("end", "Datei wird eingelesen")
            self.container.update()
            if self.parent.quelle == "csv":
                pdfgenerator.CSVgen.getMatch(self.parent.match, self.parent.inputfile)
            elif self.parent.quelle == "qsd":
                pdfgenerator.QSD.getMatch(self.parent.match, self.parent.inputfile)
            elif self.parent.quelle == "string":
                pdfgenerator.QR.getMatch(self.parent.match, self.parent.inputstring)
            self.statusbox.insert("end", "Einlesen abgeschlossen")
            self.container.update()

        self.parent.back_button["state"] = "normal"
        self.parent.ok_button["state"] = "normal"
        # self.parent.progress.stop()
        self.parent.actionOK()

    def draw_shot(self, a):

        radiusCalibre = Match.radius_dict[self.parent.match.scheibentyp][4]
        self.canvas.create_oval(
            (a.x - radiusCalibre) * self.scalefactor + self.canvsize / 2,
            -(a.y - radiusCalibre) * self.scalefactor + self.canvsize / 2,
            (a.x + radiusCalibre) * self.scalefactor + self.canvsize / 2,
            -(a.y + radiusCalibre) * self.scalefactor + self.canvsize / 2,
            # fill="orange" if a in self.parent.match.ausreisser else "green",
            fill="green",
            tag="shot",
            activefill="cyan",
        )

    def redraw_target(self):
        self.clear_target()
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
