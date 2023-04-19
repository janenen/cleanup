from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from .shooter import Shooter


@dataclass_json
@dataclass
class UserSettings:
    niceness: int = 0
    extended_analysis: bool = False


@dataclass_json
@dataclass
class User:
    data: Shooter
    settings: UserSettings

    @property
    def name(self):
        return self.data.name

    @property
    def club(self):
        return self.data.club

    @property
    def niceness(self):
        return self.settings.niceness


@dataclass_json
@dataclass
class UserList:
    users: list[User] = field(default_factory=list)
