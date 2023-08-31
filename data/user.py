from dataclasses import dataclass, field
import json
import os
import uuid
import configparser
from dataclasses_json import dataclass_json
from data.competition import Competition
from data.match import Match
from .shooter import Shooter


@dataclass_json
@dataclass
class User:
    shooter: Shooter
    niceness: int = 0
    id: str = ""
    matches: list[str] = field(default_factory=list)
    competitions: list[str] = field(default_factory=list)

    @property
    def name(self):
        return self.shooter.name

    @property
    def birthday(self):
        return self.shooter.birthday

    def add_match(self, match: Match):
        if not match.id in self.matches:
            self.matches.append(match.id)

    def add_competition(self, competition: Competition):
        if competition.id == "":
            raise Exception()
        if not competition.id in self.competitions:
            self.competitions.append(competition.id)


@dataclass_json
@dataclass
class UserDB:
    users: dict[str, User] = field(default_factory=dict)

    def save(self, file="./db/users.json"):
        if not os.path.exists(os.path.dirname(file)):
            os.mkdir(os.path.dirname(file))
        with open(file, "w") as json_file:
            json_file.write(json.dumps(json.loads(self.to_json()), indent=2))

    def load(file="./db/users.json"):
        if os.path.exists(file):
            try:
                with open(file, "r") as json_file:
                    db = UserDB.from_json(json_file.read())
            except Exception as e:
                print(e)
                print("Format not correct")
        elif os.path.exists("./schuetzen.ini"):
            print("old config found")
            db = UserDB()
            userconfig = configparser.ConfigParser()
            userconfig.read("./schuetzen.ini")

            for section in userconfig.sections():
                if not (section == "Neu" or section == "NeuerSchütze"):
                    name = userconfig.get(section, "Name")
                    niceness = userconfig.getint(section, "niceness", fallback=0)
                    db.add_user(User(shooter=Shooter(name), niceness=niceness))
            db.save(file)
            os.remove("./schuetzen.ini")
        else:
            print("User file not existing")
            db = UserDB()
            db.save(file)
        return db

    def add_user(self, user: User) -> str:
        if not user.id:
            id = str(uuid.uuid4())
            user.id = id
        if not user.id in self.users.keys():
            self.users[id] = user
        return user.id

    def _get_niceness(item: tuple[str, User]):
        return item[1].niceness

    def __getitem__(self, key):
        return self.users[key]

    def __iter__(self):
        return iter(sorted(self.users.items(), key=UserDB._get_niceness, reverse=True))
