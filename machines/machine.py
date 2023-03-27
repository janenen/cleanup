from abc import ABC, abstractmethod


class Machine(ABC):
    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, port):
        self._connection = port

    @abstractmethod
    def set_port(self, port):
        ...

    # @abstractmethod
    # def setup(self,setup):
    #    ...

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
