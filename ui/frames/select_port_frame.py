import tkinter as tk
from tkinter import ttk
from idlelib.tooltip import Hovertip
import machines


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
        self.available_machines = machines.find_machines()
        self.portlistbox.delete("0", "end")
        for machine in self.available_machines:
            self.portlistbox.insert("end", str(machine))

        self.parent.ok_button["state"] = "disabled"

    def test(self, event):
        """Handle list click event"""
        item = self.portlistbox.curselection()
        if not item:
            return
        print(item[0])
        self.parent.quelle = self.available_machines[item[0]]
        self.parent.ok_button["state"] = "normal"
        self.portlistbox.unbind("<<ListboxSelect>>")
        self.parent.actionOK()

    def reset(self, back=False):
        self.test_label.config(text="Port auswählen")
        self.portlistbox.bind("<<ListboxSelect>>", self.test)
        self.onreset = not back
        self.reload()
