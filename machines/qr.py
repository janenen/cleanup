from .machine import VirtualMachine


class QR(VirtualMachine):
    def get_string(self) -> str:
        return "QR-Code aus Eingabe"

    def config(self):
        print(self.settings)
