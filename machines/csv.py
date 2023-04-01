from .machine import VirtualMachine


class CSV(VirtualMachine):
    def get_string(self) -> str:
        return "CSV aus Datei"

    def config(self):
        print(self.settings)
