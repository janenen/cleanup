from .machine import Machine


class QR(Machine):
    def is_available(self):
        return True

    def set_port(self, port):
        print("qr")

    def get_string(self) -> str:
        return "QR-Code aus Eingabe"
