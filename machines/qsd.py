from .machine import (
    VirtualMachine,
    MachineException,
    ReadingThread,
)
from data.shot import Shot
from threading import Thread
import os
import struct


class QSDReadingThread(ReadingThread):
    def run(self):
        self.scheibentyp = self.machine.settings.type_of_target
        with open(self.machine.settings.filepath, "rb") as infile:
            bytes = infile.read(5 * 8)
            while bytes:
                double = struct.unpack("5d", bytes)
                if double == (0.0, 0.0, 0.0, 0.0, 0.0):
                    break
                self.result.append(
                    Shot(
                        ringe=round(double[0], 1),
                        teiler=int(double[3] * 10),
                        x=int(double[1]),
                        y=int(double[2]),
                    )
                )
                self._messages.append(self.result[-1])
                bytes = infile.read(5 * 8)


class QSD(VirtualMachine):
    def get_string(self) -> str:
        return "QSD aus Datei"

    def config(self):
        if not os.path.isfile(self.settings.filepath):
            raise MachineException(
                f"File {self.settings.filepath} does not exist or is not a file"
            )

    def get_reading_thread(self):
        thr = QSDReadingThread()
        thr.machine = self
        return thr
