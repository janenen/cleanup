from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Shooter:
    name: str
    birthday: str = ""
