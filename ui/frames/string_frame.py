import tkinter as tk
from tkinter import ttk
from idlelib.tooltip import Hovertip
import re


class StringFrame(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        self.container = container
        # field options
        options = {"padx": 5, "pady": 0}
        self.scrollbar = ttk.Scrollbar(self)
        self.text = tk.Text(self)
        self.scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.text.pack(side="left", fill="y")

        # add padding to the frame and show it
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def parse_text(self):
        input = self.text.get("1.0", "end")
        input = input.strip(" \r\n")
        print(input)
        if self.test_input(input):
            self.parent.inputstring = input
            return True
        else:
            return False

    def test_input(self, input):
        regex_string = "\d{8}\D{2}((\D)(\d)(\d+)([+-]\d+)([+-]\d+))+"
        return re.match(regex_string, input)

    def reset(self, back=False):
        self.parent.ok_button["state"] = "normal"
