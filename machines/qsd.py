from .machine import Machine


class QSD(Machine):
    def is_available(self):
        return True

    def set_port(self, port):
        print("qsd")

    def get_string(self) -> str:
        return "QSD aus Datei"
