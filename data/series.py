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

    def __getitem__(self, key):
        return self.shots[key]

    def __iter__(self):
        return iter(self.shots)
