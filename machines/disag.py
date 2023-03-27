from .machine import Machine

# dummy class for another physical machine
class Disag(Machine):
    def is_available(self):
        print("Diasg not found")
        return False

    def set_port(self, port):
        print("no port")

    def get_string(self) -> str:
        return "test"


if __name__ == "__main__":
    machine = Disag()
    machine.connection = None
    print(machine.is_available())
