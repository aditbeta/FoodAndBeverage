import tkinter as tk

from PIL import ImageTk, Image

from constant import red, font2, white, full_path, blue, popup_showinfo
from travel_booking_system.order import Order


class Payment(tk.Frame):
    def __init__(self, parent, booking_id, payment_option=None):
        super().__init__(parent)
        self.pack()
        self.pack_propagate(False)
        self.configure(width=1400, height=900)

        self.create_layout(payment_option)

    def create_layout(self, payment_option):
        # create grid
        configure_layout(self, payment_option)


def configure_layout(self, payment_option):
    self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
    self.columnconfigure((0, 1, 2), weight=1, uniform='a')

    # Create a label widget
    payment_frame = tk.Frame(self, width=1400, height=100,
                             background=red, padx=20, pady=20)
    payment_frame.pack()
    payment_label = tk.Label(payment_frame, text='Payment Confirmation',
                             font=font2, background=red, foreground=white)
    payment_label.grid(row=1, column=0, sticky='news')

    payment_option_frame = tk.Frame(self, width=1400, height=800,
                                    background=red, padx=20, pady=20)
    payment_option_frame.pack(side=tk.BOTTOM, fill='x')
    var = tk.StringVar(None, payment_option)
    radio_va = tk.Radiobutton(payment_option_frame, text="Virtual Account",
                              variable=var, value='virtual_account', font=font2,
                              command=lambda: reload(self, 1, 'virtual_account'))
    radio_qris = tk.Radiobutton(payment_option_frame, text="QRIS",
                                variable=var, value='qris', font=font2,
                                command=lambda: reload(self, 1, 'qris'))
    va_label = tk.Label(payment_option_frame, text='Virtual Account - Bank '
                                                   'Indonesia\nNo Virtual '
                                                   'Account: 1234567890',
                        font=font2)
    qr_image_path = Image.open(full_path('data/qr.png'))
    qr_image = ImageTk.PhotoImage(qr_image_path)
    qr_label = tk.Label(payment_option_frame, image=qr_image)
    qr_label.image = qr_image
    book_button = tk.Button(payment_option_frame, text='Book',
                            font=font2, border=0, height=1,
                            background=blue, foreground=white,
                            command=lambda: book())

    def book():
        popup_showinfo("Payment", "Payment Success\nThank you for booking with us!")
        self.destroy()
        return Order(self, 1)

    radio_va.grid(row=2, column=0, sticky='news')
    if payment_option == 'virtual_account':
        va_label.grid(row=3, column=0, sticky='news')
        radio_qris.grid(row=4, column=0, sticky='news')
        book_button.grid(row=5, column=0, sticky='news')
    elif payment_option == 'qris':
        radio_qris.grid(row=3, column=0, sticky='news')
        qr_label.grid(row=4, column=0, sticky='news')
        book_button.grid(row=5, column=0, sticky='news')
    else:
        radio_qris.grid(row=3, column=0, sticky='news')


def reload(self, booking_id, payment_option):
    self.destroy()
    return Payment(self.master, booking_id, payment_option)
