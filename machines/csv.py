from .machine import Machine


class CSV(Machine):
    def is_available(self):
        return True

    def set_port(self, port):
        print("csv")

    def get_string(self) -> str:
        return "CSV aus Datei"
