from dataclasses import dataclass, field
import json
import os
from typing import Dict
from dataclasses_json import dataclass_json
import uuid


@dataclass_json
@dataclass
class Team:
    name: str
    id: str = ""


@dataclass_json
@dataclass
class TeamDB:
    teams: Dict[str, Team] = field(default_factory=dict)

    def save(self, file="./db/teams.json"):
        with open(file, "w") as json_file:
            json.dump(
                json.loads(self.to_json()),
                json_file,
                indent=2,
            )

    def load(file="./db/teams.json"):
        if not os.path.exists(os.path.dirname(file)):
            os.mkdir(os.path.dirname(file))
        try:
            with open(file, "r") as json_file:
                db = TeamDB.from_json(json_file.read())
        except Exception as e:
            print(e)
            print("Teams file not existing")
            db = TeamDB()
            db.save(file)
        return db

    def add_team(self, team: Team) -> str:
        if not team.id:
            id = str(uuid.uuid4())
            team.id = id
        if not team.id in self.teams.keys():
            self.teams[team.id] = team
        return team.id

    def _get_name(item: tuple[str, Team]):
        return item[1].name

    def __getitem__(self, key):
        return self.teams[key]

    def __iter__(self):
        return iter(sorted(self.teams.items(), key=TeamDB._get_name))
