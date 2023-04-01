from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class MachineSettings:
    count: int
    shots_per_target: int
    type_of_target: str | None


class MachineException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Machine(ABC):
    settings: MachineSettings

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, port):
        self._connection = port

    @abstractmethod
    def set_port(self, port):
        ...

    @abstractmethod
    def config(self):
        ...

    @abstractmethod
    def is_available(self) -> bool:
        ...

    @abstractmethod
    def get_string(self) -> str:
        ...

    # @abstractmethod
    # def read(self):
    #    ...

    def __str__(self) -> str:
        return self.get_string()


class VirtualMachine(Machine):
    def is_available(self):
        return self.connection == "file"

    def set_port(self, port):
        if type(port) == str:
            self.connection = port
        else:
            self.connection = ""
