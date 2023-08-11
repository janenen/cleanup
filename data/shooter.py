from dataclasses import dataclass
from dataclasses_json import dataclass_json
from .club import Club
from .team import Team


@dataclass_json
@dataclass
class Shooter:
    name: str
    club: Club = None
    team: Team = None
