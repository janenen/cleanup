from tkinter import ttk


class FSKFrame(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        self.container = container
        self.label_list = []
        # field options
        options = {"padx": 5, "pady": 0}

        # add padding to the frame and show it
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def reset(self, back=False):
        for label in self.label_list:
            label.destroy()

        summe = 0
        for i in range(int(self.parent.fsk_schnitt) - 1, -1, -1):
            if self.parent.match.verteilung[i] == 0:
                continue
            betrag = (
                self.parent.match.verteilung[i] * (self.parent.fsk_schnitt - i) * 0.1
            )
            summe += betrag
            test_label = ttk.Label(
                self,
                text="{ring:d} : {anzahl:2d} x {price:.2f} € = {sum:2.2f} €".format(
                    ring=i,
                    anzahl=self.parent.match.verteilung[i],
                    price=(self.parent.fsk_schnitt - i) * 0.1,
                    sum=betrag,
                ),
            )
            self.label_list.append(test_label)
            test_label.pack()
        test_label = ttk.Label(self, text="----------------------".format(sum=summe))
        self.label_list.append(test_label)
        test_label.pack()
        test_label = ttk.Label(
            self, text="           Summe: {sum:2.2f} €".format(sum=summe)
        )
        self.label_list.append(test_label)
        test_label.pack()
