import tkinter as tk
import login as user
import constant as c

from constant import blue, yellow, delete_pages
from redirector import book_page, order_page, login_page


class Option(tk.Frame):
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        tk.Label(self, background=blue).pack(expand=True, fill='both')
        self.option_frame = tk.Frame(self, width=c.width * 1/8, height=c.height)
        self.option_frame.pack(side=tk.TOP, expand=True, fill='both')
        self.pack(side=tk.LEFT)
        self.pack_propagate(False)
        self.configure(width=c.width * 1/8, height=c.height)

        brand_menu_button = tk.Label(self.option_frame, text='Booking\nManagement',
                                     font=('Bold', 18), background=blue,
                                     border=1)
        brand_menu_button.place(x=0, y=0, width=c.width * 1/8, height=c.height * 1/9)

        book_menu_button = tk.Button(self.option_frame, text='Book', font=('Bold', 18),
                                     background=blue, border=0,
                                     command=lambda:
                                     indicate(book_menu_indicate, book_page))
        book_menu_button.place(x=0, y=c.height * 1/9, width=c.width * 1/8, height=c.height * 1/9)
        book_menu_indicate = tk.Label(self.option_frame, text='', bg=blue, fg='white')
        book_menu_indicate.place(x=3, y=c.height * 1/9, width=c.width * 1/160, height=c.height * 1/10)

        order_menu_button = tk.Button(self.option_frame, text='Trip', font=('Bold', 18),
                                      background=blue, border=0,
                                      command=lambda:
                                      indicate(order_menu_indicate, order_page))
        order_menu_button.place(x=0, y=c.height * 2/9, width=c.width * 1/8, height=c.height * 1/9)
        order_menu_indicate = tk.Label(self.option_frame, text='', bg=blue)
        order_menu_indicate.place(x=3, y=c.height * 2/9, width=c.width * 1/160, height=c.height * 1/10)

        if user.user_id < 1:
            login_menu_button = tk.Button(self.option_frame, text='Login', font=('Bold', 18),
                                          background=blue, border=0,
                                          command=lambda:
                                          indicate(login_menu_indicate,
                                                   login_page))
            login_menu_button.place(x=0, y=c.height * 3/9, width=c.width * 1/8, height=c.height * 1/9)
            login_menu_indicate = tk.Label(self.option_frame, text='', bg=blue)
            login_menu_indicate.place(x=3, y=c.height * 3/9, width=c.width * 1/160, height=c.height * 1/10)

        exit_menu_button = tk.Button(self.option_frame, text='Exit', font=('Bold', 18),
                                     background=blue, border=0,
                                     command=self.master.destroy)
        exit_menu_button.place(x=0, y=400, width=c.width * 1/8, height=c.height * 1/9)

        def indicate(lb, page):
            hide_indicate()
            lb.config(bg=yellow)
            delete_pages(main_frame)
            page(main_frame, user.user_id)

        def hide_indicate():
            book_menu_indicate.config(bg=blue)
            order_menu_indicate.config(bg=blue)
            login_menu_indicate.config(bg=blue)
