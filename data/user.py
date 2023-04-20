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
    shooter: Shooter
    settings: UserSettings

    @property
    def name(self):
        return self.shooter.name

    @property
    def club(self):
        return self.shooter.club

    @property
    def niceness(self):
        return self.settings.niceness


@dataclass_json
@dataclass
class UserList:
    users: list[User] = field(default_factory=list)

    def save(self):
        with open("./users.json", "w") as json_file:
            json_file.write(self.to_json())

    def add_user(self, user: User):
        self.users.append(user)
