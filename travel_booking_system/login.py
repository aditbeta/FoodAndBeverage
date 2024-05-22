import tkinter as tk
import constant as c

from book import Book
from constant import write_append, font1, df_by_col, \
    delete_pages, read_csv, popup_showinfo, default_source, default_destination, default_date

email_header = 'email'
phone_header = 'phone'
password_header = 'password'

user_df = read_csv('data/user.csv')
user_id = -1
logged_email = ''


class Login(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_frame = parent
        self.pack()
        self.pack_propagate(False)
        self.configure(width=c.width, height=c.height)

        configure_layout(self, False)

    def login(self, email, password):
        if ((user_df[email_header] == email) & (
                user_df[password_header] == password)).any():
            global logged_email
            logged_email = email
            redirect_to_book_page(self, 'Login Success\nWelcome, ')
        else:
            popup_showinfo("Login", "Login failed")

    def register_page(self):
        self.destroy()
        Register(self.master)


class Register(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        self.pack_propagate(False)
        self.configure(width=c.width, height=c.height)

        configure_layout(self, True)

    def register_user(self, email, phone, password):
        if (user_df[email_header] == email).any():
            popup_showinfo("Register Failed", "Username already exists")
        else:
            write_append('data/user.csv', user_df,
                         [0, email, phone, password])
            popup_showinfo("Register Success", "Welcome, " + email)
            self.destroy()
            Book(self.master, get_user_id(email))


def configure_layout(self, is_register):
    if user_id > 0:
        redirect_to_book_page(self, 'You are logged in as ')

    self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
    self.columnconfigure((0, 1, 2), weight=1, uniform='a')

    # Create a label widget
    email_label = tk.Label(self, text='Email', font=font1)
    email_field = tk.Entry(self, font=font1)
    phone_label = tk.Label(self, text='Phone', font=font1)
    phone_field = tk.Entry(self, font=font1)
    password_label = tk.Label(self, text='Password', font=font1)
    password_field = tk.Entry(self, show='*', font=font1)

    # Place the label in the window
    email_label.grid(row=1, column=0, sticky='news')
    email_field.grid(row=1, column=1, columnspan=2, pady=20,
                     sticky='news')

    if not is_register:
        login_button = tk.Button(
                self, text='Login', font=font1, border=0, command=lambda:
                self.login(email_field.get(), password_field.get()))
        register_label = tk.Label(self, text='Don\'t have an account?',
                                  font=font1)
        register_button = tk.Button(self, text='Register', font=font1,
                                    border=0,
                                    command=lambda: self.register_page())

        password_label.grid(row=2, column=0, sticky='news')
        password_field.grid(row=2, column=1, columnspan=2, pady=20,
                            sticky='news')
        login_button.grid(row=3, column=0, columnspan=3, sticky='news')
        register_label.grid(row=4, column=0, columnspan=2, sticky='news')
        register_button.grid(row=4, column=2, sticky='news')
    else:
        register_button = tk.Button(
                self, text='Register', font=font1, border=0, command=lambda:
                self.register_user(email_field.get(), phone_field.get(),
                                   password_field.get()))

        phone_label.grid(row=2, column=0, sticky='news')
        phone_field.grid(row=2, column=1, columnspan=2, pady=20,
                         sticky='news')
        password_label.grid(row=3, column=0, sticky='news')
        password_field.grid(row=3, column=1, columnspan=2, pady=20,
                            sticky='news')
        register_button.grid(row=4, column=0, columnspan=3, sticky='news')


def get_user_id(email):
    global user_id
    user_id = df_by_col(user_df, email_header, email)['id']
    return user_id


def redirect_to_book_page(self, message):
    popup_showinfo('Welcome to Travel Booking System', message + logged_email)
    delete_pages(self.main_frame)
    Book(self.main_frame, get_user_id(logged_email), default_source, default_destination, default_date)
