from .shot import Shot
import statistics
from dataclasses import dataclass, field


@dataclass
class Series:
    shots: list[Shot] = field(default_factory=list)

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

    # def __init__(self, zehntel):
    #    self.shots = []
    #    self.anzahl = 0
    #    self.summe = 0
    #    self.summe_ganz = 0
    #    self.ablageRL = 0
    #    self.ablageHT = 0
    #    self.best = Shot()
    #    self.worst = Shot()
    #    self.zehntel = zehntel
    #    self.ausreisser = []
    #    self.verteilung = [0] * 11
    #    # self.update()
    #
    # def update(self):
    #    self.anzahl = len(self.shots)
    #    self.summe = 0
    #    self.summe_ganz = 0
    #    self.ablageRL = 0
    #    self.ablageHT = 0
    #    self.verteilung = [0] * 11
    #    if self.anzahl > 0:
    #        self.best = max(self.shots)
    #        self.worst = min(self.shots)
    #    for s in self.shots:
    #        self.summe = self.summe + s.ringe
    #        self.summe_ganz = self.summe_ganz + math.floor(s.ringe)
    #        self.ablageRL = self.ablageRL + s.x / self.anzahl
    #        self.ablageHT = self.ablageHT + s.y / self.anzahl
    #        self.verteilung[int(s.ringe)] += 1
    #
    # def addShot(self, shot):
    #    self.shots.append(shot)
    #    self.update()
    #
    # def getOutliers(self, l=0.5):
    #    self.ausreisser = []
    #    data = np.array([[A.x, A.y] for A in self.shots])
    #    scores = (
    #        loop.LocalOutlierProbability(data, n_neighbors=3)
    #        .fit()
    #        .local_outlier_probabilities
    #    )
    #    for shot, prob in zip(self.shots, scores):
    #        if prob > l:
    #            self.ausreisser.append(shot)
    #
    # def __str__(self):
    #    retval = ""
    #    for s in self.shots:
    #        retval = retval + str(s) + " "
    #    return retval
    #
    # def __repr__(self):
    #    retval = ""
    #    for s in self.shots:
    #        retval = retval + str(s) + " "
    #    return retval

    def __getitem__(self, key):
        return self.shots[key]

    def __iter__(self):
        return iter(self.shots)
