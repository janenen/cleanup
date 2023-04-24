from dataclasses import dataclass, field
import statistics
from dataclasses_json import dataclass_json
from .shot import Shot
from .series import Series
from .shooter import Shooter
import math

RADIUS_DICT = {
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
}  #


@dataclass_json
@dataclass
class MatchSettings:
    competition: str
    decimal: bool
    count: int
    date: str
    shooter: Shooter
    type_of_target: str


@dataclass_json
@dataclass
class Match:
    settings: MatchSettings
    shots: list[Shot] = field(default_factory=list)

    @property
    def result(self):
        return (
            sum([s.ringe for s in self.shots])
            if self.settings.decimal
            else sum([s.ringe_ganz for s in self.shots])
        )

    @property
    def best(self):
        return max(self.shots)

    @property
    def worst(self):
        return min(self.shots)

    @property
    def ablageRL(self):
        return statistics.mean([s.x for s in self.shots])

    @property
    def ablageHT(self):
        return statistics.mean([s.y for s in self.shots])

    @property
    def summe(self):
        return sum([s.ringe for s in self.shots])

    @property
    def summe_ganz(self):
        return sum([s.ringe_ganz for s in self.shots])

    @property
    def anzahl(self):
        return len(self.shots)

    @property
    def series(self):
        return [
            Series(self.shots[n * 10 : n * 10 + 10]) for n in range(self.anzahl // 10)
        ]

    # def __init__(self, settings):
    #    self.settings = settings
    #    self.series = []
    #    self.anzahl = 0
    #    self.summe = 0
    #    self.summe_ganz = 0
    #    self.ablageRL = 0
    #    self.ablageHT = 0
    #    self.best = Shot()
    #    self.worst = Shot()
    #    # self.zehntel = False
    #    # self.bewerb = "Training"
    #    # self.name = ""
    #    # self.verein = ""
    #
    #    # self.datum = date.today().strftime("%d.%m.%Y")
    #    self.ausreisser = []
    #    self.verteilung = [0] * 11

    # def update(self):
    #    self.anzahl = 0
    #    self.summe = 0
    #    self.summe_ganz = 0
    #    self.ablageRL = 0
    #    self.ablageHT = 0
    #    self.best = None
    #    self.worst = None
    #    bestShots = []
    #    worstShots = []
    #    self.verteilung = [0] * 11
    #
    #    for series in self.series:
    #        series.update()
    #        self.anzahl += series.anzahl
    #        self.summe += series.summe
    #        self.summe_ganz += series.summe_ganz
    #        self.ablageRL += series.ablageRL / len(self.series)
    #        self.ablageHT += series.ablageHT / len(self.series)
    #        bestShots.append(series.best)
    #        worstShots.append(series.worst)
    #        self.verteilung = list(map(add, self.verteilung, series.verteilung))
    #
    #    if self.anzahl > 0:
    #        self.best = max(bestShots)
    #        self.worst = min(worstShots)

    def get_x_list(self):
        return [s.x for s in self]

    def get_y_list(self):
        return [s.y for s in self]

    def get_t_list(self):
        return [s.teiler for s in self]

    def get_r_list(self):
        return [s.ringe for s in self]

    # def getOutliers(self, l=0.5):
    #    if self.anzahl > 4:
    #        self.ausreisser = []
    #        for series in self.series:
    #            series.getOutliers(l)
    #            self.ausreisser.extend(series.ausreisser)

    # def addSeries(self, series:Series):
    #    self.series.append(series)
    #    #self.update()

    # def fromShotlist(self, shotlist:list[Shot]):
    #    self.series = []
    #    if len(shotlist) > 0:
    #        for i in range(0, int((len(shotlist) - 1) / 10) + 1):
    #            self.addSeries(Series(self.settings.decimal))
    #        for n, shot in enumerate(shotlist):
    #            self.series[int(n / 10)].addShot(shot)
    #    self.update()

    def countRing(self, wert):
        n = 0
        for s in self:
            if math.floor(s.ringe) == wert:
                n += 1
        return n

    def __str__(self):
        retval = ""
        retval += f"{self.settings.shooter.name} {self.settings.type_of_target} {self.settings.date}\r\n"
        for ser in self.series:
            retval = retval + str(ser) + "\r\n"
        return retval

    def __iter__(self):
        return self.__generatorfunction()

    def __generatorfunction(self):
        for shot in self.shots:
            yield shot
