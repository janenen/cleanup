from .machine import Machine
import serial.tools.list_ports


def find_machines() -> list[Machine]:
    from .rika import Rika
    from .disag import Disag
    from .csv import CSV
    from .qsd import QSD
    from .qr import QR

    known_machines = [
        Rika,
        Disag,
        CSV,
        QR,
        QSD,
    ]
    ports = serial.tools.list_ports.comports(True) + ["file"]
    machines: list[Machine] = []
    for machine in known_machines:
        new_machine = machine()
        print(machine)
        for port in ports:
            print(port)
            try:
                new_machine.set_port(port)
            except:
                continue
            if new_machine.is_available():
                machines.append(new_machine)
    return machines
