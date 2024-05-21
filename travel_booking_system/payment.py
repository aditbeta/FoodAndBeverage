import locale
import tkinter as tk

from PIL import ImageTk, Image

from constant import red, font2, white, full_path, blue, popup_showinfo, \
    df_by_id, order_df, booking_df, write_update, schedule_df, route_df
from ticket import Ticket


class Payment(tk.Frame):
    def __init__(self, parent, order_id, booking_id, payment_option=None):
        super().__init__(parent)
        self.pack()
        self.pack_propagate(False)
        self.configure(width=1400, height=900)
        self.order_id = order_id
        self.booking_id = booking_id

        self.create_layout(payment_option)

    def create_layout(self, payment_option):
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')

        booking = df_by_id(booking_df, self.booking_id)
        schedule = df_by_id(schedule_df, booking['schedule_id'])
        route = df_by_id(route_df, schedule['route_id'])

        date = booking['date'] + ' ' + schedule['departure']
        seat = booking['seat'].split(';')
        locale.setlocale(locale.LC_ALL, 'id_ID')
        price = locale.currency(schedule['price'] * len(seat), grouping=True)
        trip_detail = 'Trip Detail: ' + route['source_code'] + ' - ' + route[
            'destination_code'] + ' ' + date

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
        trip_label = tk.Label(payment_option_frame, text=trip_detail)
        trip_label.pack(side=tk.TOP, fill='x')
        selected_label = tk.Label(payment_option_frame,
                                  text='Selected seat: ' + ','.join(seat))
        selected_label.pack(side=tk.TOP, fill='x')
        price_label = tk.Label(payment_option_frame, text='Price: ' + price)
        price_label.pack(side=tk.TOP, fill='x')

        var = tk.StringVar(None, payment_option)
        radio_va = tk.Radiobutton(payment_option_frame, text="Virtual Account",
                                  variable=var, value='virtual_account',
                                  font=font2,
                                  command=lambda: self.reload('virtual_account'))
        radio_qris = tk.Radiobutton(payment_option_frame, text="QRIS",
                                    variable=var, value='qris', font=font2,
                                    command=lambda: self.reload('qris'))
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
            write_update('data/order.csv', order_df, self.order_id - 1,
                         'is_paid', True)
            popup_showinfo("Payment",
                           "Payment Success\nThank you for booking with us!")
            self.destroy()
            return Ticket(self.master, self.order_id)

        radio_va.pack(side=tk.TOP, fill='x')
        if payment_option == 'virtual_account':
            va_label.pack(side=tk.TOP, fill='x')
            radio_qris.pack(side=tk.TOP, fill='x')
            book_button.pack(side=tk.TOP, fill='x')
        elif payment_option == 'qris':
            radio_qris.pack(side=tk.TOP, fill='x')
            qr_label.pack(side=tk.TOP, fill='x')
            book_button.pack(side=tk.TOP, fill='x')
        else:
            radio_qris.pack(side=tk.TOP, fill='x')

    def reload(self, payment_option):
        self.destroy()
        return Payment(
                self.master, self.order_id, self.booking_id, payment_option)
