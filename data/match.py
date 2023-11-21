from dataclasses import dataclass, field
import json
import os
import statistics
import uuid
from dataclasses_json import dataclass_json

from .shot import Shot
from .series import Series
from .shooter import Shooter
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.competition import Competition

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
class Match:
    shooter: Shooter
    type_of_target: str
    date: str
    shots: list[Shot] = field(default_factory=list)
    id: str = ""
    club: str = ""
    team: str = ""
    competitions: list[str] = field(default_factory=list)

    def get_result(self, decimal: bool = False):
        return round(self.summe if decimal else self.summe_ganz, 1)

    @property
    def best(self) -> Shot:
        return max(self.shots)

    @property
    def worst(self) -> Shot:
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
            Series(self.shots[n * 10 : n * 10 + 10])
            for n in range(0, (self.anzahl - 1) // 10 + 1)
        ]

    def get_x_list(self):
        return [s.x for s in self]

    def get_y_list(self):
        return [s.y for s in self]

    def get_t_list(self):
        return [s.teiler for s in self]

    def get_r_list(self):
        return [s.ringe for s in self]

    def countRing(self, wert):
        n = 0
        for s in self:
            if math.floor(s.ringe) == wert:
                n += 1
        return n

    def add_competition(self, competition: "Competition"):
        if not competition.id in self.competitions:
            self.competitions.append(competition.id)

    def __str__(self):
        retval = ""
        retval += f"{self.shooter.name} {self.type_of_target} {self.date}\r\n"
        for ser in self.series:
            retval = retval + str(ser) + "\r\n"
        return retval

    def __iter__(self):
        return self.__generatorfunction()

    def __generatorfunction(self):
        for shot in self.shots:
            yield shot


MATCH_DB_VERSION = 1


@dataclass_json
@dataclass
class MatchDB:
    matches: dict[str, Match] = field(default_factory=dict)
    version: int | None = None

    def save(self, file="./db/matches.json"):
        with open(file, "w") as json_file:
            json_file.write(json.dumps(json.loads(self.to_json()), indent=2))

    def load(filepath="./db/matches.json"):
        if not os.path.exists(os.path.dirname(filepath)):
            os.mkdir(os.path.dirname(filepath))
        try:
            with open(filepath, "r") as json_file:
                db = MatchDB.from_json(json_file.read())
            if not db.version == MATCH_DB_VERSION:
                if db.version == None:
                    matches = None
                    with open(filepath) as file:
                        matches = json.load(file)
                        for key in matches["matches"].keys():
                            for shot in matches["matches"][key]["shots"]:
                                if type(shot["teiler"]) == int:
                                    shot["teiler"] = shot["teiler"] / 10
                                    shot["x"] = shot["x"] / 100
                                    shot["y"] = shot["y"] / 100
                        matches["version"] = 1
                    with open(filepath, "w") as file:
                        json.dump(matches, file, indent=2)
                    return MatchDB.load(filepath)
                # elif provide upgrade from version n-1
        except Exception as e:
            print(e)
            print("Matches file not existing")
            db = MatchDB(version=MATCH_DB_VERSION)
            db.save(filepath)
        return db

    def add_match(self, match: Match) -> str:
        if not match.id:
            id = str(uuid.uuid4())
            match.id = id
        if not match.id in self.matches.keys():
            self.matches[match.id] = match
        return match.id

    def __getitem__(self, key):
        return self.matches[key]

    def __iter__(self):
        return iter(self.matches.items())
