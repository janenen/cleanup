from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
from threading import Thread
from data.shot import Shot


@dataclass
class MachineSettings:
    count: int | None
    shots_per_target: int | None
    type_of_target: str | None
    filepath: str | None


class MachineException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Machine(ABC):
    settings: MachineSettings
    _connection: str

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

    def __str__(self) -> str:
        return self.get_string()


class VirtualMachine(Machine):
    def is_available(self):
        return self.connection == "file"  # and os.path.isfile(self.settings.filepath)

    def set_port(self, port):
        if type(port) == str:
            self.connection = port
        else:
            self.connection = ""


class ReadingThread(Thread):
    _messages = []
    machine: Machine
    result = []
    scheibentyp = None

    def get_reading(self):
        try:
            return self._messages.pop(0), self.scheibentyp  # Workaround fix later
        except IndexError:
            return None, None

    def is_finished(self):
        return not self.is_alive() and not self._messages

    def get_result(self) -> list[Shot]:
        if self.is_finished():
            return self.result
