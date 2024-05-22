import tkinter as tk

from book import Book
from menu import Option
from constant import width, height, \
    default_source, default_destination, default_date


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

        self.book = Book(self, None, default_source, default_destination, default_date)
        self.option = Option(self, self.book)

        # run
        self.mainloop()


App("Menu", (width, height))
