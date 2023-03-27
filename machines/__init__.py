from .rika import Rika
from .disag import Disag
from .csv import CSV
from .qsd import QSD
from .qr import QR
from .machine import Machine
import serial.tools.list_ports

known_machines = [Rika, Disag, CSV, QR, QSD]


def find_machines() -> list[Machine]:
    ports = serial.tools.list_ports.comports(True)
    machines = []
    for port in ports:
        print(port)
        for machine in known_machines:
            print(machine)
            new_machine = machine()
            new_machine.set_port(port)
            if new_machine.is_available():
                machines.append(new_machine)
    return machines
