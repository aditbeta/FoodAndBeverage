import tkinter as tk

from constant import write_append, font1, df_by_col, \
    delete_pages, read_csv


class Payment(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        self.pack_propagate(False)
        self.configure(width=1400, height=900)

        self.create_layout()

    def create_layout(self):
        # create grid
        configure_layout(self)


def configure_layout(self):
    self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
    self.columnconfigure((0, 1, 2), weight=1, uniform='a')

    # Create a label widget
    payment_label = tk.Label(self, text='Payment Confirmation', font=font1)
    payment_label.grid(row=1, column=0, sticky='news')


    # email_field = tk.Entry(self, font=font1)
    # phone_label = tk.Label(self, text='Phone', font=font1)
    # phone_field = tk.Entry(self, font=font1)
    # password_label = tk.Label(self, text='Password', font=font1)
    # password_field = tk.Entry(self, show='*', font=font1)

    # Place the label in the window
    # email_field.grid(row=1, column=1, columnspan=2, pady=20,
    #                  sticky='news')

    # if not is_register:
    #     login_button = tk.Button(
    #             self, text='Login', font=font1, border=0, command=lambda:
    #             self.login(email_field.get(), password_field.get()))
    #     register_label = tk.Label(self, text='Don\'t have an account?',
    #                               font=font1)
    #     register_button = tk.Button(self, text='Register', font=font1,
    #                                 border=0,
    #                                 command=lambda: self.register_page())
    #
    #     password_label.grid(row=2, column=0, sticky='news')
    #     password_field.grid(row=2, column=1, columnspan=2, pady=20,
    #                         sticky='news')
    #     login_button.grid(row=3, column=0, columnspan=3, sticky='news')
    #     register_label.grid(row=4, column=0, columnspan=2, sticky='news')
    #     register_button.grid(row=4, column=2, sticky='news')
    # else:
    #     register_button = tk.Button(
    #             self, text='Register', font=font1, border=0, command=lambda:
    #             self.register_user(email_field.get(), phone_field.get(),
    #                                password_field.get()))
    #
    #     phone_label.grid(row=2, column=0, sticky='news')
    #     phone_field.grid(row=2, column=1, columnspan=2, pady=20,
    #                      sticky='news')
    #     password_label.grid(row=3, column=0, sticky='news')
    #     password_field.grid(row=3, column=1, columnspan=2, pady=20,
    #                         sticky='news')
    #     register_button.grid(row=4, column=0, columnspan=3, sticky='news')
