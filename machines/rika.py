from .machine import Machine, MachineException
import serial, time, re
from serial.tools.list_ports_common import ListPortInfo
from threading import Thread
from data.shot import Shot

NUL = b"\x00"
SOH = b"\x01"
EOT = b"\x04"
ACK = b"\x06"
_REPEAT = b"\x07"
BS = b"\x08"
FF = b"\x0C"
CR = b"\x0D"
SYN = b"\x16"
ESC = b"\x1B"
ABM = b"\xD0"
EINZEL = b"\xD1"
_10SER = b"\xD2"
GESAMT = b"\xD3"
_5SER = b"\xD4"
REST = b"\xD5"


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
            ret = Match()
            ret.scheibentyp = self.scheibentyp
            ret.fromShotlist(self.result)
            return ret

    def run(self):
        first = True
        regex_string = "b'(?P<serial>\\d{8})\\\\r(?P<bus_address>\\d{3})\\\\r(?P<manual_code>\\d{8})\\\\r(?P<type_of_target>\\w{2})\\\\r(?P<distance_factor>\\d{2})\\\\r(?P<count>\\d{3})\\\\r(?P<value>\\d{3})\\\\r(?P<distance>\\d{5})\\\\r(?P<x>[+-]\\d{5})\\\\r(?P<y>[+-]\\d{5})\\\\r(?P<checksum>.*)'"
        regex = re.compile(regex_string)
        with self.machine.connection as conn:
            while len(self.result) < self.machine.settings.count:
                conn.write(SYN)
                ans = conn.read(1)
                if ans == SOH:
                    groupdict = regex.match(str(conn.read(32 + 24 + 2))).groupdict()
                    if first:
                        self.scheibentyp = groupdict["type_of_target"]
                        first = False
                    self.result.append(
                        Shot(
                            ringe=int(groupdict["value"]) / 10,
                            teiler=int(groupdict["distance"]),
                            x=int(groupdict["x"]),
                            y=int(groupdict["y"]),
                        )
                    )
                    self._messages.append(self.result[-1])
                    conn.write(FF)  # FF
                else:
                    time.sleep(0.2)
            conn.write(ABM)
            conn.read(1)


class Rika(Machine):
    def is_available(self):
        with self.connection as conn:
            conn.read()
            conn.write(EINZEL)  # d1 einzeltreffer
            ans = conn.read(3)
            conn.write(ABM)
            conn.read(1)
            return ans == b"200"

    def set_port(self, port):
        if type(port) == ListPortInfo:
            self.connection = serial.Serial(port.name, 9600, timeout=0.5)

    def get_string(self) -> str:
        return f"Rika SAG-2 an {self._connection.name}"

    def config(self):
        with self.connection as conn:
            conn.read()  # flush buffer
            conn.write(EINZEL)  # d1 einzeltreffer
            ans = conn.read(3)
            if ans != b"200":
                raise MachineException("Rika antwortet nicht")
            # ESC S XXX CR
            conn.write(
                ESC + b"S" + bytes(str(self.settings.count).zfill(3), "utf-8") + CR
            )
            ans = conn.read(1)
            if ans != ACK:
                conn.write(ABM)
                raise MachineException("Anzahl konnte nicht übernommen werden")
            # ESC U X CR
            conn.write(
                ESC
                + b"U"
                + bytes(str(self.settings.shots_per_target).zfill(1), "utf-8")
                + CR
            )
            ans = conn.read(1)
            if ans != ACK:
                conn.write(ABM)
                raise MachineException(
                    "Schuss pro Scheibe konnte nicht übernommen werden"
                )
            # ESC Z 3 CR
            conn.write(ESC + b"Z3" + CR)
            ans = conn.read(1)
            if ans != ACK:
                conn.write(ABM)
                raise MachineException("Teilerwertung konnte nicht übernommen werden")

    def get_reading_thread(self):
        thr = ReadingThread()
        thr.machine = self
        return thr
