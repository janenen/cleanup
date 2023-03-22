import math
from datetime import date
import numpy as np
from PyNomaly import loop
from operator import add
import csv


class Shot:
    def __init__(self, **kwargs):
        # def __init__(self,ringe,teiler,x,y):
        self.ringe = kwargs.get("ringe", None)
        self.teiler = kwargs.get("teiler", 9999999)
        self.x = kwargs.get("x", None)
        self.y = kwargs.get("y", None)
        # self.k_distance = None
        # self.k_nearest = []
        # self.lrd = None
        # self.lof = None
        # self.ringe=ringe
        # self.teiler=teiler
        # self.x=x
        # self.y=y

    def __str__(self):
        return f"{self.ringe}"

    def __repr__(self):
        return f"{self.ringe}"

    def __lt__(self, other):
        return self.teiler > other.teiler


class Series:
    def __init__(self, zehntel):
        self.shots = []
        self.anzahl = 0
        self.summe = 0
        self.summe_ganz = 0
        self.ablageRL = 0
        self.ablageHT = 0
        self.best = Shot()
        self.worst = Shot()
        self.zehntel = zehntel
        self.ausreisser = []
        self.verteilung = [0] * 11
        # self.update()

    def update(self):
        self.anzahl = len(self.shots)
        self.summe = 0
        self.summe_ganz = 0
        self.ablageRL = 0
        self.ablageHT = 0
        self.verteilung = [0] * 11
        if self.anzahl > 0:
            self.best = max(self.shots)
            self.worst = min(self.shots)
        for s in self.shots:
            self.summe = self.summe + s.ringe
            self.summe_ganz = self.summe_ganz + math.floor(s.ringe)
            self.ablageRL = self.ablageRL + s.x / self.anzahl
            self.ablageHT = self.ablageHT + s.y / self.anzahl
            self.verteilung[int(s.ringe)] += 1

    def addShot(self, shot):
        self.shots.append(shot)
        self.update()

    def getOutliers(self, l=0.5):
        self.ausreisser = []
        data = np.array([[A.x, A.y] for A in self.shots])
        # print(data)
        scores = (
            loop.LocalOutlierProbability(data, n_neighbors=3)
            .fit()
            .local_outlier_probabilities
        )
        # print(scores)
        for shot, prob in zip(self.shots, scores):
            if prob > l:
                self.ausreisser.append(shot)

    def __str__(self):
        retval = ""
        for s in self.shots:
            retval = retval + str(s) + " "
        return retval

    def __repr__(self):
        retval = ""
        for s in self.shots:
            retval = retval + str(s) + " "
        return retval

    def __getitem__(self, key):
        return self.shots[key]

    def __iter__(self):
        return iter(self.shots)


class Match:
    radius_dict = {
        "LP": (575, 250, 800, 2975, 225),
        "KK": (520, 250, 800, 5620, 280),
        "LG": (25, -25, 250, 1520, 225),
        "ZS": (225, 0, 450, 2025, 232),  # eigentlich 232,5
        "LS": (275, 25, 125, 1525, 225),
        "K3": (
            312,
            150,
            480,
            3372,
            280,
        ),  # aus KK 50m berechnet, weicht möglicherweise ab
        "AB": (300, 25, 600, 4500, 300),  # Armbrust 30m international
        "AD": (100, 0, 450, 1450, 225),  # keine Daten gefunden
        "BS": (100, 0, 450, 1450, 225),
    }  # luftgewehrscheibe

    def __init__(self):
        self.series = []
        self.anzahl = 0
        self.summe = 0
        self.summe_ganz = 0
        self.ablageRL = 0
        self.ablageHT = 0
        self.best = Shot()
        self.worst = Shot()
        self.zehntel = False
        self.bewerb = "Training"
        self.name = ""
        self.verein = ""
        self.scheibentyp = ""
        self.datum = date.today().strftime("%d.%m.%Y")
        self.ausreisser = []
        self.verteilung = [0] * 11

    def update(self):
        self.anzahl = 0
        self.summe = 0
        self.summe_ganz = 0
        self.ablageRL = 0
        self.ablageHT = 0
        self.best = None
        self.worst = None
        bestShots = []
        worstShots = []
        self.verteilung = [0] * 11

        for series in self.series:
            series.update()
            self.anzahl += series.anzahl
            self.summe += series.summe
            self.summe_ganz += series.summe_ganz
            self.ablageRL += series.ablageRL / len(self.series)
            self.ablageHT += series.ablageHT / len(self.series)
            bestShots.append(series.best)
            worstShots.append(series.worst)
            self.verteilung = list(map(add, self.verteilung, series.verteilung))

        if self.anzahl > 0:
            self.best = max(bestShots)
            self.worst = min(worstShots)

    def get_x_list(self):
        return [s.x for s in self]

    def get_y_list(self):
        return [s.y for s in self]

    def get_t_list(self):
        return [s.teiler for s in self]

    def get_r_list(self):
        return [s.ringe for s in self]

    def getOutliers(self, l=0.5):
        if self.anzahl > 4:
            self.ausreisser = []
            for series in self.series:
                series.getOutliers(l)
                self.ausreisser.extend(series.ausreisser)

    def addSeries(self, series):
        self.series.append(series)
        self.update()

    def fromShotlist(self, shotlist, zehntel=None):
        if zehntel != None:
            self.zehntel = zehntel
        self.series = []
        if len(shotlist) > 0:
            for i in range(0, int((len(shotlist) - 1) / 10) + 1):
                self.addSeries(Series(zehntel))
            for n, shot in enumerate(shotlist):
                self.series[int(n / 10)].addShot(shot)
        self.update()
        # print(self.series)

    def setZehntel(self, zehntel):
        self.zehntel = zehntel
        self.update()

    def countRing(self, wert):
        n = 0
        for s in self:
            if math.floor(s.ringe) == wert:
                n += 1
        return n

    def __str__(self):
        retval = ""
        for ser in self.series:
            retval = retval + str(ser) + "\r\n"
        return retval

    def __repr__(self):
        retval = ""
        for ser in self.series:
            retval = retval + str(ser) + "\r\n"
        return retval

    def __getitem__(self, key):
        return self.series[key]

    def __setitem__(self, key, value):
        self.series[key] = value

    def __iter__(self):
        # self.__generatorfunction()
        return self.__generatorfunction()

    def __generatorfunction(self):
        for series in self.series:
            for shot in series:
                yield shot

    # def __next__(self):
    #    return next(self.__generatorfunction())
