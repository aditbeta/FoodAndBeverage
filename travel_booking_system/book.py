import locale
import tkinter as tk

from tkcalendar import DateEntry

from constant import white, font2, red, blue, black, \
    default_result_frame, default_tree, booking_df, schedule_df, route_df, \
    location_df, vehicle_df, df_by_col, green, df_val, yellow, write_append, \
    write_update
from order import order_df
from payment import Payment


class Book(tk.Frame):
    def __init__(
            self, parent, user_id=None, source=None, destination=None,
            date=None, book=False, schedule=None, booking=None, vehicle=None):
        super().__init__(parent)
        self.user_id = user_id
        self.df_dict = None
        self.date = date
        self.destination = destination
        self.source = source
        self.tree = None
        self.result_frame = tk.Frame(self, width=1400, height=800)
        self.sources, self.destinations = self.read_locations()
        self.pack(side=tk.RIGHT)
        self.pack_propagate(False)
        self.configure(width=1400, height=900)

        self.create_search_frame(source, destination, date, book, schedule,
                                 booking, vehicle)

    def create_search_frame(
            self, source=None, destination=None, date=None,
            book=False, schedule=None, booking=None, vehicle=None):
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

        if book:
            self.create_book_layout(schedule, booking)
        else:
            self.create_result_layout(self.source, self.destination,
                                      self.date, False)

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
            self.source = source
            self.destination = destination
            self.date = date
            return self.reload()

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

    def create_book_layout(self, schedule, booking):
        self.result_frame.pack(side=tk.BOTTOM, fill='x')
        back_button = tk.Button(self.result_frame, text='Back',
                                font=font2, border=0, height=1,
                                background=blue, foreground=white,
                                command=lambda: self.reload())
        back_button.pack(side=tk.TOP, fill='x')
        book_button = tk.Button(self.result_frame, text='Book',
                                font=font2, border=0, height=1,
                                background=blue, foreground=white,
                                command=lambda: book())
        book_button.pack(side=tk.TOP, fill='x')
        selected_label = tk.Label(self.result_frame, text='Selected seat: ')
        selected_label.pack(side=tk.TOP, fill='x')
        price_label = tk.Label(self.result_frame, text='Price: Rp0,00')
        price_label.pack(side=tk.TOP, fill='x')

        seat_frame = tk.Frame(self.result_frame, width=1000, height=400)
        seat_frame.pack(side=tk.TOP)

        i = 1
        row1 = [4]
        row2 = [1, 2, 3]
        row3 = [1, 2, 4]
        row4 = [1, 2, 4]
        row5 = [1, 2, 3, 4]
        selected = []
        booked_seat = []
        if not booking.empty:
            booked_seat = df_val(booking, 'seat').split(';')
        for x in range(5):
            for y in range(4):
                if y + 1 in eval('row' + str(x + 1)):
                    if str(i) in booked_seat:
                        btn = tk.Button(seat_frame, fg=white, bg=red, text=i)
                        btn['state'] = tk.DISABLED
                    else:
                        btn = tk.Button(seat_frame, bg=yellow, text=i)
                        btn["command"] = lambda btn=btn: click(btn)
                    i += 1
                else:
                    btn = tk.Button(seat_frame, bg='white')
                    btn['state'] = tk.DISABLED
                btn.config(width=5, height=5)
                btn.grid(column=x, row=y, sticky='news')

        for x in range(5):
            tk.Grid.columnconfigure(seat_frame, x, weight=1)

        for y in range(4):
            tk.Grid.rowconfigure(seat_frame, y, weight=1)

        def click(button):
            seat = str(button["text"])
            if seat in selected:
                selected.remove(seat)
            else:
                selected.append(seat)
            selected_label["text"] = "Selected seat: " + ", ".join(selected)
            price = locale.currency(schedule['price'] * len(selected),
                                    grouping=True)
            price_label["text"] = "Price: " + price
            if button["bg"] == yellow:
                button["bg"] = green
                button["fg"] = white
            else:
                button["bg"] = yellow
                button["fg"] = black

        def book():
            selected_seat = ";".join(selected)

            if not booking.empty:
                booking_id = df_val(booking, 'id')
                updated_booked_seat = ';'.join(booked_seat + selected)
                write_update('data/booking.csv', booking_df, booking_id - 1,
                             'seat', updated_booked_seat)
            else:
                booking_id = write_append(
                        'data/booking.csv', booking_df,
                        [0, schedule['id'], self.date, selected_seat])

            order_id = write_append('data/order.csv', order_df,
                                    [0, int(self.user_id), booking_id,
                                     selected_seat, False])

            self.destroy()
            return Payment(self.master, order_id, booking_id, 'virtual_account')

    def book_route(self, event):
        selected = self.tree.item(self.tree.focus())

        col = self.tree.identify_column(event.x)

        if col != '#6':
            return

        return self.reload(True, self.df_dict[selected['values'][-1]][0],
                           self.df_dict[selected['values'][-1]][1])

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
        hidden_columns = ("ID",)
        columns = ("Vehicle", "Departure", "Arrival", "Price",
                   "Available Seats", "Action")
        tree = default_tree(self.result_frame, columns + hidden_columns)
        tree["displaycolumns"] = columns
        tree.bind('<ButtonRelease-1>', self.book_route)

        locale.setlocale(locale.LC_ALL, 'id_ID')

        df_dict = {}
        for i, schedule in schedules.iterrows():
            vehicle = df_by_col(vehicle_df, 'code', schedule['vehicle_code'])
            bookings = booking_df.query('schedule_id == @schedule.id '
                                        'and date == @date')
            df_dict[schedule['id']] = [schedule, bookings]
            available_seat = vehicle['seat']
            if not bookings.empty:
                booked_seat = df_val(bookings, 'seat').split(';')
                available_seat -= len(booked_seat)
            tree.insert('', 'end', values=(
                vehicle['name'], schedule['departure'], schedule['arrival'],
                locale.currency(schedule['price'], grouping=True),
                available_seat, 'Book', schedule['id']))

        tree.pack(fill='x')
        self.tree = tree
        self.df_dict = df_dict

    def reload(self, book=False, schedule=None, booking=None):
        self.destroy()
        return Book(self.master, self.user_id, self.source, self.destination,
                    self.date,
                    book, schedule, booking)
