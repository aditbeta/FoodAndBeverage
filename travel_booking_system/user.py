import tkinter as tk
from tkinter.messagebox import showinfo
import pandas as pd

from travel_booking_system.book import Book

id_header = 'email'
email_header = 'email'
phone_header = 'phone'
password_header = 'password'

user_dataframe = pd.read_csv('data/user.csv')
user_id = 0


class Login(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        self.pack_propagate(False)
        self.configure(width=1400, height=900)

        self.create_layout()

    def create_layout(self):
        # create grid
        configure_layout(self, False)

    def login(self, email, password):
        if ((user_dataframe[email_header] == email) & (
                user_dataframe[password_header] == password)).any():
            Book(self)
        else:
            popup_showinfo("Login", "Login failed")

    def register_page(self):
        self.destroy()
        Register(self.master)


def register_user(email, password):
    if (user_dataframe[email_header] == email).any():
        print('Username exists')
    else:
        last_id = len(user_dataframe.index)
        user_dataframe.loc[last_id] = [last_id+1, email, last_id+1, password]
        user_dataframe.to_csv(
                'data/user.csv', mode='w', index=False, header=True)
        print('Registered successfully')


class Register(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        self.pack_propagate(False)
        self.configure(width=1400, height=900)

        self.create_layout()

    def create_layout(self):
        # create grid
        configure_layout(self, True)


def configure_layout(self, is_register):
    self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
    self.columnconfigure((0, 1, 2), weight=1, uniform='a')

    # Create a label widget
    email_label = tk.Label(self, text='Email', font=('Bold', 18))
    email_field = tk.Entry(self, font=('Bold', 18))
    password_label = tk.Label(self, text='Password', font=('Bold', 18))
    password_field = tk.Entry(self, show='*', font=('Bold', 18))

    # Place the label in the window
    email_label.grid(row=1, column=0, sticky='news')
    email_field.grid(row=1, column=1, columnspan=2, pady=20,
                     sticky='news')
    password_label.grid(row=2, column=0, sticky='news')
    password_field.grid(row=2, column=1, columnspan=2, pady=20,
                        sticky='news')

    if not is_register:
        login_button = tk.Button(self, text='Login', font=('Bold', 18),
                                 border=0, command=lambda: self.login(
                    email_field.get(), password_field.get()))
        register_label = tk.Label(self, text='Don\'t have an account?',
                                  font=('Bold', 18))
        register_button = tk.Button(self, text='Register', font=('Bold', 18),
                                    border=0,
                                    command=lambda: self.register_page())
        login_button.grid(row=3, column=0, columnspan=3, sticky='news')
        register_label.grid(row=4, column=0, columnspan=2, sticky='news')
        register_button.grid(row=4, column=2, sticky='news')
    else:
        register_button = tk.Button(self, text='Register', font=('Bold', 18),
                                    border=0, command=lambda: register_user(
                    email_field.get(), password_field.get()))
        register_button.grid(row=3, column=0, columnspan=3, sticky='news')


def popup_showinfo(title, message):
    showinfo(title, message)
