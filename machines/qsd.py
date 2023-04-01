from .machine import VirtualMachine


class QSD(VirtualMachine):
    def get_string(self) -> str:
        return "QSD aus Datei"

    def config(self):
        print(self.settings)
