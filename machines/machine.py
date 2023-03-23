from typing import Protocol


class Machine(Protocol):
    def setup(self,setup):
        ...
        
    def config(self, config):
        ...

    def is_available(self) -> bool:
        ...

    def read(self):
        ...
