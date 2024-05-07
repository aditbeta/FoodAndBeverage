import tkinter as tk

from booking_management.constant import bg_gray, bg_blue
from booking_management.book import Book
from booking_management.trip import Trip
from booking_management.user import Login


class Option(tk.Frame):
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        tk.Label(self, background='#c3c3c3').pack(expand=True, fill='both')
        self.pack(side=tk.LEFT)
        self.pack_propagate(False)
        self.configure(width=200, height=900)

        brand_menu_button = tk.Button(self, text='Booking\nManagement',
                                      font=('Bold', 18), background='#c3c3c3',
                                      border=1)
        brand_menu_button.place(x=0, y=0, width=200, height=100)

        book_menu_button = tk.Button(self, text='Book', font=('Bold', 18),
                                     background=bg_gray, border=0,
                                     command=lambda:
                                     indicate(book_menu_indicate, book_page))
        book_menu_button.place(x=0, y=100, width=200, height=100)
        book_menu_indicate = tk.Label(self, text='', bg=bg_gray)
        book_menu_indicate.place(x=3, y=100, width=10, height=90)

        trip_menu_button = tk.Button(self, text='Trip', font=('Bold', 18),
                                     background=bg_gray, border=0,
                                     command=lambda:
                                     indicate(trip_menu_indicate, trip_page))
        trip_menu_button.place(x=0, y=200, width=200, height=100)
        trip_menu_indicate = tk.Label(self, text='', bg=bg_gray)
        trip_menu_indicate.place(x=3, y=200, width=10, height=90)

        login_menu_button = tk.Button(self, text='Login', font=('Bold', 18),
                                      background=bg_gray, border=0,
                                      command=lambda:
                                      indicate(login_menu_indicate, login_page))
        login_menu_button.place(x=0, y=300, width=200, height=100)
        login_menu_indicate = tk.Label(self, text='', bg=bg_gray)
        login_menu_indicate.place(x=3, y=300, width=10, height=90)

        exit_menu_button = tk.Button(self, text='Exit', font=('Bold', 18),
                                     background=bg_gray, border=0,
                                     command=self.master.destroy)
        exit_menu_button.place(x=0, y=400, width=200, height=100)

        def indicate(lb, page):
            hide_indicate()
            lb.config(bg=bg_blue)
            delete_pages()
            page()

        def hide_indicate():
            book_menu_indicate.config(bg=bg_gray)
            trip_menu_indicate.config(bg=bg_gray)
            login_menu_indicate.config(bg=bg_gray)

        def delete_pages():
            for frame in main_frame.winfo_children():
                frame.destroy()

        def book_page():
            Book(main_frame)

        def trip_page():
            Trip(main_frame)

        def login_page():
            Login(main_frame)
