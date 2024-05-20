import tkinter as tk

import pandas as pd

from constant import default_result_frame, default_tree, \
    booking_df, schedule_df, route_df, vehicle_df, location_df, df_by_id, \
    df_by_col, read_csv

from datetime import datetime

order_df = read_csv('data/order.csv')


class Order(tk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.user_id = user_id
        self.order_frame = tk.Frame(self, width=1400, height=800)
        self.pack(side=tk.RIGHT)
        self.pack_propagate(False)
        self.configure(width=1400, height=900)

        self.create_tree_result()

    def create_tree_result(self):
        self.order_frame.pack(side=tk.TOP, fill='x')

        if self.user_id < 1:
            default_result_frame(
                    self.order_frame, 'Please login first.')
            return

        orders = order_df.query('user_id == @self.user_id')
        if orders.empty:
            default_result_frame(
                    self.order_frame, 'You don\'t have any order yet.')
            return

        # Add a Treeview widget
        columns = ("Source", "Destination", "Date", "Vehicle", "Status")
        tree = default_tree(self.order_frame, columns)

        for i, order in orders.iterrows():
            booking = df_by_id(booking_df, order['booking_id'])
            schedule = df_by_id(schedule_df, booking['schedule_id'])
            route = df_by_id(route_df, schedule['route_id'])
            source = df_by_col(
                    location_df, 'code', route['source_code'])['name']
            destination = df_by_col(
                    location_df, 'code', route['destination_code'])['name']
            vehicle = (df_by_col(
                    vehicle_df, 'code', schedule['vehicle_code'])['name']
                       + ' ' + order['seat'])
            date = booking['date'] + ' ' + schedule['departure']
            is_passed = False
            now = datetime.now()
            if datetime.strptime(date, '%Y-%m-%d %H:%M') < now:
                is_passed = True
            status = 'Completed' if is_passed else 'Upcoming'
            if not order['is_paid']:
                status = 'Expired' if is_passed else 'Awaiting Payment'

            tree.insert('', 'end', values=(
                source, destination, date, vehicle, status))

        tree.pack(fill='x')
