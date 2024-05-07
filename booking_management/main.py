import tkinter as tk

from booking_management.book import Book
from booking_management.menu import Option


class App(tk.Tk):
    def __init__(self, title, size):
        # setup
        super().__init__()

        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        x = int((screenwidth - size[0]) / 2)
        y = int((screenheight - size[1]) / 2)
        self.title(title)
        self.geometry('%dx%d+%d+%d' % (size[0], size[1], x, y))
        self.minsize(size[0], size[1])

        # menu
        self.main = Book(self)
        self.option = Option(self, self.main)

        # run
        self.mainloop()


App("Menu", (1600, 900))