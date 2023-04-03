from .machine import (
    VirtualMachine,
    MachineException,
    ReadingThread,
)
from data.shot import Shot
import re

header_regex_string = "\d{8}\w{2}"
shots_regex_string = (
    "(?P<ring>\D)(?P<tenth>\d)(?P<teiler>\d+)(?P<x>[+-]\d+)(?P<y>[+-]\d+)"
)


class QRReadingThread(ReadingThread):
    def run(self):
        def unmap_ring(instr: str) -> str:
            return (
                instr.replace("A", "10.")
                .replace("B", "9.")
                .replace("C", "8.")
                .replace("D", "7.")
                .replace("E", "6.")
                .replace("F", "5.")
                .replace("G", "4.")
                .replace("H", "3.")
                .replace("I", "2.")
                .replace("J", "1.")
            )

        y = self.machine.settings.filepath[4:8]
        m = self.machine.settings.filepath[2:4]
        d = self.machine.settings.filepath[0:2]
        datum = f"{d}.{m}.{y}"  # ignore for now (refactoring of settings required)
        self.scheibentyp = self.machine.settings.filepath[8:10]
        str_shots = self.machine.settings.filepath[10:]
        for shot in re.finditer(shots_regex_string, str_shots):
            print("Ringe:" + unmap_ring(shot["ring"]) + shot["tenth"])
            self.result.append(
                Shot(
                    ringe=float(unmap_ring(shot["ring"]) + shot["tenth"]),
                    teiler=int(shot["teiler"]),
                    x=int(shot["x"]),
                    y=int(shot["y"]),
                )
            )
            self._messages.append(self.result[-1])


class QR(VirtualMachine):
    def get_string(self) -> str:
        return "QR-Code aus Eingabe"

    def config(self):
        if not re.search(shots_regex_string, self.settings.filepath):
            raise MachineException("Format of header of QR-Code does not match")
        if not re.search(shots_regex_string, self.settings.filepath):
            raise MachineException(f"Format of entries of QR-Code does not match")

    def get_reading_thread(self):
        thr = QRReadingThread()
        thr.machine = self
        return thr
