from datetime import date
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from data.shot import Shot
from .match import Match, MatchSettings
from .shooter import Shooter
from machines.machine import Machine


@dataclass_json
@dataclass
class CompetitionSettings:
    name: str
    date: str
    count: int
    shots_per_target: int
    type_of_target: int
    decimal: bool


@dataclass_json
@dataclass
class Competition:
    settings: CompetitionSettings
    entries: list[Match] = field(default_factory=list)

    def add_match(self, shooter: Shooter, shots: list[Shot]) -> Match:
        new_match = self.create_match(shooter, shots)
        self.entries.append(new_match)
        return new_match

    def create_match(self, shooter: Shooter, shots: list[Shot]) -> Match:
        return Match(
            MatchSettings(
                competition=self.settings.name,
                decimal=self.settings.decimal,
                count=self.settings.count,
                date=date.today().strftime("%d.%m.%Y"),
                shooter=shooter,
                type_of_target=self.settings.type_of_target,
            ),
            shots,
        )

    def get_sorted_results(self):
        return self.entries
        # add sort function later
