import tkinter as tk
from datetime import datetime

from constant import default_result_frame, default_tree, \
    booking_df, schedule_df, route_df, vehicle_df, location_df, df_by_id, \
    df_by_col, order_df
from travel_booking_system.payment import Payment


class Order(tk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.tree = None
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
        hidden_columns = ("Order ID", "Booking ID")
        columns = ("Source", "Destination", "Date", "Vehicle", "Status")
        tree = default_tree(self.order_frame, columns + hidden_columns)
        tree["displaycolumns"] = columns
        tree.bind('<ButtonRelease-1>', self.payment)

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

            tree.insert('', 'end', values=(source, destination, date, vehicle,
                                           status,
                                           order['id'], order['booking_id']))

        tree.pack(fill='x')
        self.tree = tree

    def payment(self, event):
        selected = self.tree.item(self.tree.focus())

        col = self.tree.identify_column(event.x)

        if col != '#5':
            return

        self.destroy()
        return Payment(self.master, selected['values'][-2], selected['values'][-1], 'virtual_account')
