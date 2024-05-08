import tkinter as tk


class Trip(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='red')
        # tk.Label(self, text="TRIP", background='#c3c3c3').pack(
        #         expand=True, fill='both')
        self.bg = 'red'
        self.pack(side=tk.RIGHT)
        self.pack_propagate(False)
        self.configure(width=1400, height=900)
