from dataclasses import dataclass


@dataclass
class Shooter:
    name: str
    club: str | None
    team: str | None
