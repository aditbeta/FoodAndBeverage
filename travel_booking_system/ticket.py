import locale
import tkinter as tk
import constant as c

from constant import font1, full_path, df_by_id, order_df, booking_df, \
    schedule_df, vehicle_df, route_df, location_df, df_by_col

from PIL import ImageTk, Image


class Ticket(tk.Frame):
    def __init__(self, parent, order_id):
        super().__init__(parent)
        self.pack()
        self.pack_propagate(False)
        self.configure(width=c.width * 7/8, height=c.height)
        self.order_id = order_id

        self.configure_layout()

    def configure_layout(self):
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')

        order = df_by_id(order_df, self.order_id)
        booking = df_by_id(booking_df, order['booking_id'])
        schedule = df_by_id(schedule_df, booking['schedule_id'])
        vehicle = df_by_col(vehicle_df, 'code', schedule['vehicle_code'])
        route = df_by_id(route_df, schedule['route_id'])
        source = df_by_col(location_df, 'code', route['source_code'])
        destination = df_by_col(location_df, 'code', route['destination_code'])
        seats = order['seat'].split(';')

        trip_text = source['name'] + ' - ' + destination['name']
        date_text = (schedule['departure'] + ' - ' + schedule['arrival']
                     + ' ' + booking['date'])
        vehicle_text = vehicle['name'] + ' [' + ','.join(seats) + ']'
        locale.setlocale(locale.LC_ALL, 'id_ID')
        payment_text = locale.currency(schedule['price'] * len(seats), grouping=True)
        status_text = 'Paid' if order['is_paid'] else 'Unpaid'

        # Create a label widget
        trip_label = tk.Label(self, text='Trip Detail: ', font=font1)
        trip_value = tk.Label(self, text=trip_text, font=font1)
        date_label = tk.Label(self, text='Date: ', font=font1)
        date_value = tk.Label(self, text=date_text, font=font1)
        vehicle_label = tk.Label(self, text='Vehicle:', font=font1)
        vehicle_value = tk.Label(self, text=vehicle_text, font=font1)
        payment_label = tk.Label(self, text='Payment:', font=font1)
        payment_value = tk.Label(self, text=payment_text, font=font1)
        status_label = tk.Label(self, text='Status:', font=font1)
        status_value = tk.Label(self, text=status_text, font=font1)
        qr_image_path = Image.open(full_path('data/qr.png'))
        qr_image = ImageTk.PhotoImage(qr_image_path)
        qr_label = tk.Label(self, image=qr_image)
        qr_label.image = qr_image

        # Place the label in the window
        trip_label.grid(row=1, column=0, sticky='news')
        trip_value.grid(row=1, column=1, columnspan=2, pady=20, sticky='news')
        date_label.grid(row=2, column=0, sticky='news')
        date_value.grid(row=2, column=1, columnspan=2, pady=20, sticky='news')
        vehicle_label.grid(row=3, column=0, sticky='news')
        vehicle_value.grid(row=3, column=1, columnspan=2, pady=20, sticky='news')
        payment_label.grid(row=4, column=0, sticky='news')
        payment_value.grid(row=4, column=1, columnspan=2, pady=20, sticky='news')
        status_label.grid(row=4, column=0, sticky='news')
        status_value.grid(row=4, column=1, columnspan=2, pady=20, sticky='news')
        qr_label.grid(row=5, column=0, columnspan=3, pady=20, sticky='news')
