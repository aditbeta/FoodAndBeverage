import tkinter as tk
import travel_booking_system.user as user

from travel_booking_system.book import Book
from travel_booking_system.constant import blue, yellow, delete_pages
from travel_booking_system.order import Order
from travel_booking_system.user import Login


class Option(tk.Frame):
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        tk.Label(self, background=blue).pack(expand=True, fill='both')
        self.pack(side=tk.LEFT)
        self.pack_propagate(False)
        self.configure(width=200, height=900)

        brand_menu_button = tk.Label(self, text='Booking\nManagement',
                                     font=('Bold', 18), background=blue,
                                     border=1)
        brand_menu_button.place(x=0, y=0, width=200, height=100)

        book_menu_button = tk.Button(self, text='Book', font=('Bold', 18),
                                     background=blue, border=0,
                                     command=lambda:
                                     indicate(book_menu_indicate, book_page))
        book_menu_button.place(x=0, y=100, width=200, height=100)
        book_menu_indicate = tk.Label(self, text='', bg=blue, fg='white')
        book_menu_indicate.place(x=3, y=100, width=10, height=90)

        order_menu_button = tk.Button(self, text='Trip', font=('Bold', 18),
                                      background=blue, border=0,
                                      command=lambda:
                                      indicate(order_menu_indicate, order_page))
        order_menu_button.place(x=0, y=200, width=200, height=100)
        order_menu_indicate = tk.Label(self, text='', bg=blue)
        order_menu_indicate.place(x=3, y=200, width=10, height=90)

        if user.user_id < 1:
            login_menu_button = tk.Button(self, text='Login', font=('Bold', 18),
                                          background=blue, border=0,
                                          command=lambda:
                                          indicate(login_menu_indicate,
                                                   login_page))
            login_menu_button.place(x=0, y=300, width=200, height=100)
            login_menu_indicate = tk.Label(self, text='', bg=blue)
            login_menu_indicate.place(x=3, y=300, width=10, height=90)

        exit_menu_button = tk.Button(self, text='Exit', font=('Bold', 18),
                                     background=blue, border=0,
                                     command=self.master.destroy)
        exit_menu_button.place(x=0, y=400, width=200, height=100)

        def indicate(lb, page):
            hide_indicate()
            lb.config(bg=yellow)
            delete_pages(main_frame)
            page()

        def hide_indicate():
            book_menu_indicate.config(bg=blue)
            order_menu_indicate.config(bg=blue)
            login_menu_indicate.config(bg=blue)

        def book_page():
            Book(main_frame, user.user_id)

        def order_page():
            Order(main_frame, user.user_id)

        def login_page():
            Login(main_frame)
