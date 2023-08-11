
import tkinter as tk
from tkinter import ttk
from data.user import User
from idlelib.tooltip import Hovertip


class SelectUserFrame(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        
        options = {"padx": 5, "pady": 0}
        self.scrollbar = tk.Scrollbar(self)
        self.userlistbox = tk.Listbox(self, height=10, width=50)

        def onselect(event):
            self.select()

        self.userlistbox.bind("<<ListboxSelect>>", onselect)
        self.userlistbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.userlistbox.yview)
        self.scrollbar.grid(column=2, row=0, sticky="wens")
        self.userlistbox.grid(columnspan=2, column=0, row=0, sticky="ew")

        self.test_label = ttk.Label(self, text="")
        self.test_label.grid(columnspan=2, column=0, row=2, sticky="nesw", **options)
        self.new_button = ttk.Button(self, text="Neuer Benutzer")
        self.new_button.grid(column=1, row=3, sticky="e", **options)
        Hovertip(self.new_button, "Neuen Benutzer anlegen")
        self.new_button.configure(command=self.new)

        self.edit_button = ttk.Button(self, text="Bearbeiten")
        self.edit_button.grid(column=2, row=3, sticky="e", **options)
        Hovertip(self.edit_button, "Benutzer bearbeiten")
        self.edit_button.configure(command=self.edit)
        self.columnconfigure(0, weight=1)

        # add padding to the frame and show it
        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
        self.edit_shooter = False
        self.create_new_user=False

    def select(self, event):
        self.edit_shooter = False
        self.create_new_user=False
        selection = self.userlistbox.curselection()
        if len(selection) > 0:
            n = selection[0]
            if n < len(self.parent.userlist.users):
                self.parent.user = sorted(
                    self.parent.userlist.users, key=self.get_niceness, reverse=True
                )[n]
                self.test_label.config(text=self.parent.user.name)
                self.edit_button["state"] = "normal"
            else:
                pass
                #self.edit_shooter = True
                #self.test_label.config(text="Neuer Schütze")
                #self.edit_button["state"] = "disabled"
        self.parent.back_button["state"] = "normal"
        self.parent.ok_button["state"] = "normal"

    def reset(self, back=False):
        self.test_label.config(text="Schütze auswählen")
        self.parent.user = None
        

        self.userlistbox.delete("0", "end")

        for user in sorted(
            self.parent.userlist.users, key=self.get_niceness, reverse=True
        ):
            self.userlistbox.insert("end", user.name)

        #self.userlistbox.insert("end", "Neuer Schütze")
        self.userlistbox.bind("<<ListboxSelect>>", self.select)
        self.parent.back_button["state"] = "disabled"
        self.parent.ok_button["state"] = "disabled"
        self.edit_button["state"] = "disabled"

    def get_niceness(self, user: User):
        if user.niceness:
            return user.niceness
        else:
            return 0

    def edit_user(self):
        self.userlistbox.unbind("<<ListboxSelect>>")
        return self.edit_shooter
    def new_user(self):
        self.parent.user=None
        self.userlistbox.unbind("<<ListboxSelect>>")
        return self.create_new_user

    def edit(self):
        self.edit_shooter = True
        self.parent.actionOK()

    def new(self):
        self.create_new_user = True
        self.parent.actionOK()
