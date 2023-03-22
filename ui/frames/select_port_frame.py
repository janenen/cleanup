import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
from idlelib.tooltip import Hovertip


class SelectPortFrame(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent

        options = {"padx": 5, "pady": 0}
        self.portscrollbar = tk.Scrollbar(self)
        self.portlistbox = tk.Listbox(
            self, height=10, width=50, yscrollcommand=self.portscrollbar.set
        )
        self.portscrollbar.config(command=self.portlistbox.yview)
        self.portscrollbar.grid(column=2, row=0, sticky="wens")
        self.portlistbox.grid(columnspan=2, column=0, row=0, sticky="ew")

        self.reload_button = ttk.Button(self, text="Reload")
        self.reload_button.grid(column=1, row=1, sticky="e", **options)
        Hovertip(self.reload_button, "Liste der verfügbaren Ports neu laden")
        self.reload_button.configure(command=self.reload)

        self.test_label = ttk.Label(self, text="")
        self.test_label.grid(column=0, row=1, sticky="w", **options)

        # add padding to the frame and show it
        self.columnconfigure(0, weight=1)
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def reload(self):
        self.ports = serial.tools.list_ports.comports(True)
        self.portlistbox.delete("0", "end")
        for port in self.ports:
            self.portlistbox.insert("end", "{}: {}".format(port.name, port.description))
        self.portlistbox.insert("end", "Aus Datei")
        self.portlistbox.insert("end", "QR-Code")
        self.parent.ok_button["state"] = "disabled"
        # self.test(event=None,port=self.ports[0])

    def test(self, event):
        """Handle list click event"""
        item = self.portlistbox.curselection()
        if not item:
            return
        if self.portlistbox.get(item[0]) == "Aus Datei":
            self.test_label.config(text="Aus Datei")
            self.parent.quelle = "file"
            self.parent.ok_button["state"] = "normal"
            self.portlistbox.unbind("<<ListboxSelect>>")
            self.parent.actionOK()

        elif self.portlistbox.get(item[0]) == "QR-Code":
            self.test_label.config(text="QR-Code")
            self.parent.quelle = "string"
            self.parent.ok_button["state"] = "normal"
            self.portlistbox.unbind("<<ListboxSelect>>")
            self.parent.actionOK()

        else:
            port = self.ports[item[0]]

            self.parent.ser = serial.Serial(port.device, 9600, timeout=0.5)
            self.parent.ser.write(b"\xd3")
            ans = self.parent.ser.read(3)
            if ans == b"200":
                self.parent.quelle = "maschine"
                self.test_label.config(text="RIKA gefunden")
                self.parent.ser.write(b"\xd0")
                self.parent.ser.read(1)
                self.parent.ser.close()
                self.parent.ok_button["state"] = "normal"
                self.portlistbox.unbind("<<ListboxSelect>>")
                self.parent.actionOK()

            else:
                self.test_label.config(text="RIKA nicht gefunden")
                self.parent.ok_button["state"] = "disabled"
            self.parent.ser.close()

    def reset(self, back=False):
        self.test_label.config(text="Port auswählen")
        self.portlistbox.bind("<<ListboxSelect>>", self.test)
        self.onreset = not back
        self.reload()
