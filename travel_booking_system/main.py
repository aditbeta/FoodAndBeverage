import tkinter as tk
import constant as c

from book import Book
from menu import Option
from constant import set_screen


class App(tk.Tk):
    def __init__(self, title, size):
        # setup
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = int(screen_width * 2/3)
        height = int(screen_height * 2/3)
        set_screen(width, height)
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.title(title)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.minsize(width, height)

        self.book = Book(self, None, c.default_source, c.default_destination, c.default_date)
        self.option = Option(self, self.book)

        # run
        self.mainloop()


App("Menu", (c.width, c.height))
