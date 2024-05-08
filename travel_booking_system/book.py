import tkinter as tk
from tkcalendar import DateEntry

import locale

from travel_booking_system.constant import white, font2, red, blue, black, \
    default_result_frame, default_tree, booking_df, schedule_df, route_df, \
    location_df, vehicle_df, df_by_col


class Book(tk.Frame):
    def __init__(self, parent, source=None, destination=None, date=None):
        super().__init__(parent)
        self.result_frame = tk.Frame(self, width=1400, height=800)
        self.sources, self.destinations = self.read_locations()
        self.pack(side=tk.RIGHT)
        self.pack_propagate(False)
        self.configure(width=1400, height=900)

        self.create_search_frame(source, destination, date)

    def create_search_frame(self, source=None, destination=None, date=None):
        self.rowconfigure((0, 1), weight=1, uniform='a')
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform='a')
        self.pack_propagate(False)

        search_frame = tk.Frame(self, width=1400, height=100,
                                background=red, padx=20, pady=20)
        search_frame.pack(side=tk.TOP, fill='x')

        # create input layout
        source_label = tk.Label(search_frame, text='Source', font=font2,
                                background=red, foreground=white)
        source_click = tk.StringVar(value=source) if source else tk.StringVar()
        source_field = tk.OptionMenu(search_frame, source_click, *self.sources)
        source_field.config(bg=white, fg=black, font=font2, width=20)
        source_option = source_field.nametowidget(source_field.menuname)
        source_option.config(bg=white, fg=black, font=font2)
        spacer_label = tk.Label(search_frame, text='-', font=font2,
                                background=red, foreground=white)
        destination_label = tk.Label(search_frame, text='Destination',
                                     font=font2,
                                     background=red, foreground=white)
        destination_click = tk.StringVar(value=destination) \
            if destination else tk.StringVar(search_frame)
        destination_field = tk.OptionMenu(search_frame, destination_click,
                                          *self.destinations)
        destination_field.config(bg=white, fg=black, font=font2, width=20)
        destination_option = destination_field.nametowidget(
                destination_field.menuname)
        destination_option.config(bg=white, fg=black, font=font2)
        date_label = tk.Label(search_frame, text='Date', font=font2,
                              background=red, foreground=white)
        date_field = DateEntry(search_frame, date_pattern='yyyy-mm-dd')
        if date:
            date_field.delete(0, 'end')
            date_field.insert(0, date)

        self.create_result_layout(source_click.get(), destination_click.get(),
                                  date_field.get(), False)

        search_button = tk.Button(search_frame, text='Search',
                                  font=font2, border=0, height=1,
                                  background=blue, foreground=white,
                                  command=lambda: self.create_result_layout(
                                          source_click.get(),
                                          destination_click.get(),
                                          date_field.get(),
                                          True))

        # layout field
        source_label.grid(row=0, column=0, columnspan=2)
        source_field.grid(row=1, column=0, columnspan=2, padx=10)
        spacer_label.grid(row=1, column=2)
        destination_label.grid(row=0, column=3, columnspan=2)
        destination_field.grid(row=1, column=3, columnspan=2, padx=10)
        date_label.grid(row=0, column=5, columnspan=2)
        date_field.grid(row=1, column=5, columnspan=2)
        search_button.grid(row=1, column=7, padx=10)

    def create_result_layout(self, source, destination, date, refresh):
        if refresh:
            self.destroy()
            return Book(self.master, source, destination, date)

        self.result_frame.pack(side=tk.BOTTOM, fill='x')

        valid, source, destination = self.map_locations(
                source, destination)
        if not valid:
            return

        valid, schedules = self.read_schedules(
                source, destination, date)
        if not valid:
            return

        self.create_tree_result(schedules, date)

    def book_route(self, event):
        pass
        # selected = self.tree.item(self.tree.focus())
        #
        # col = self.tree.identify_column(event.x)
        # print('curItem = ', selected)
        # print('col = ', col)
        #
        # if col == '#0':
        #     cell_value = selected['text']
        # elif col == '#1':
        #     cell_value = selected['values'][0]
        # elif col == '#2':
        #     cell_value = selected['values'][1]
        # elif col == '#3':
        #     cell_value = selected['values'][2]

    @staticmethod
    def read_locations():
        source_codes = route_df['source_code'].tolist()
        destination_codes = route_df['destination_code'].tolist()
        sources = location_df.query('code in @source_codes')['name'].tolist()
        destinations = location_df.query('code in @destination_codes')[
            'name'].tolist()

        return sources, destinations

    def map_locations(self, source, destination):
        valid = True
        source_location = location_df.query('name == @source')
        if not source_location.empty:
            source = source_location.iloc[0]['code']
        destination_location = location_df.query('name == @destination')
        if not destination_location.empty:
            destination = destination_location.iloc[0]['code']
        if not source or not destination:
            default_result_frame(
                    self.result_frame, 'Source or destination not found')
            valid = False

        return valid, source, destination

    def read_schedules(self, source, destination, date):
        routes = route_df.query(
                'source_code == @source and destination_code == @destination '
                'and start_date <= @date and end_date >= @date')
        route_ids = routes['id'].tolist()
        schedules = schedule_df.query('route_id in @route_ids')

        if schedules.empty:
            default_result_frame(
                    self.result_frame, 'No result found for this route')
            return False, None

        return True, schedules

    def create_tree_result(self, schedules, date):
        # Add a Treeview widget
        columns = ("Vehicle", "Departure", "Arrival", "Price",
                   "Available Seats", "Action")
        tree = default_tree(self.result_frame, columns)
        tree.bind('<ButtonRelease-1>', self.book_route)

        locale.setlocale(locale.LC_ALL, 'id_ID')

        for i, schedule in schedules.iterrows():
            vehicle = df_by_col(vehicle_df, 'code', schedule['vehicle_code'])
            bookings = booking_df.query('schedule_id == @schedule.id '
                                        'and date == @date')
            available_seat = vehicle['seat']
            if not bookings.empty:
                booked_seat = bookings.iloc[0]['seat'].split(';')
                available_seat -= len(booked_seat)
            tree.insert('', 'end', values=(
                vehicle['name'], schedule['departure'],
                schedule['arrival'],
                locale.currency(schedule['price'], grouping=True),
                available_seat, 'Book'))

        tree.pack(fill='x')
