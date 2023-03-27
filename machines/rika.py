from .machine import Machine
import serial


class Rika(Machine):
    def is_available(self):
        with self.connection as conn:
            conn.read()
            conn.write(b"\xd1")  # d1 einzeltreffer
            ans = conn.read(3)
            conn.write(b"\xd0")
            conn.read(1)
            return ans == b"200"

    def set_port(self, port):
        self.connection = serial.Serial(port.name, 9600, timeout=0.5)

    def get_string(self) -> str:
        return f"Rika SAG-2 an {self._connection.name}"


if __name__ == "__main__":
    import serial

    port = "COM4"
    machine = Rika()
    machine.connection = serial.Serial(port, 9600, timeout=0.5)
    print(machine.is_available())
