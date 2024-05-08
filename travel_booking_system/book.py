import tkinter as tk
from tkinter import ttk

import pandas as pd
from tkcalendar import DateEntry

vehicle_dataframe = pd.read_csv('data/vehicle.csv')
location_dataframe = pd.read_csv('data/location.csv')
route_dataframe = pd.read_csv('data/route.csv')


class Book(tk.Frame):
    def __init__(self, parent, source=None, destination=None, date=None):
        super().__init__(parent)
        self.pack(side=tk.RIGHT)
        self.pack_propagate(False)
        self.configure(width=1400, height=900)

        self.create_search_layout(source, destination, date)

    def create_search_layout(self, source=None, destination=None, date=None):
        self.rowconfigure((0, 1), weight=1, uniform='a')
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform='a')
        self.pack_propagate(False)

        search_frame = tk.Frame(self, width=1400, height=100,
                                background='#e5a3a3', padx=20, pady=20)
        search_frame.pack(side=tk.TOP, fill='x')

        # create field
        source_label = tk.Label(search_frame, text='Source', font=('Bold', 14))
        source_field = tk.Entry(search_frame, font=('Bold', 14))
        spacer_label = tk.Label(search_frame, text='<=>', font=('Bold', 14))
        destination_label = tk.Label(search_frame, text='Destination',
                                     font=('Bold', 14))
        destination_field = tk.Entry(search_frame, font=('Bold', 14))
        date_label = tk.Label(search_frame, text='Date', font=('Bold', 14))
        date_field = DateEntry(search_frame, date_pattern='yyyy-mm-dd')
        if source:
            source_field.insert(0, source)
        if destination:
            destination_field.insert(0, destination)
        if date:
            date_field.delete(0, 'end')
            date_field.insert(0, date)
        self.create_result_layout(source_field.get(), destination_field.get(),
                                  date_field.get(), False)

        search_button = tk.Button(search_frame, text='Search',
                                  font=('Bold', 14), border=0, pady=10,
                                  command=lambda: self.create_result_layout(
                                          source_field.get(),
                                          destination_field.get(),
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

        result = route_dataframe.query(
                'source_code == @source and destination_code == @destination '
                'and start_date <= @date and end_date >= @date')

        result_frame = tk.Frame(self, width=1400, height=800)
        result_frame.pack(side=tk.BOTTOM, fill='x')

        scroll_y = tk.Scrollbar(result_frame, orient='vertical')
        scroll_y.pack(side='right', fill='y')
        scroll_x = tk.Scrollbar(result_frame, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 12))
        style.configure("Treeview", font=(None, 16))
        style.configure('Treeview', rowheight=100)

        # Add a Treeview widget
        tree = ttk.Treeview(result_frame,
                            column=("Vehicle", "Departure", "Arrival", "Price",
                                    "Available Seats", "Action"),
                            show='headings', height=800,
                            yscrollcommand=scroll_y.set,
                            xscrollcommand=scroll_x.set, selectmode="none")
        tree.column("# 1", anchor=tk.CENTER)
        tree.heading("# 1", text="Vehicle")
        tree.column("# 2", anchor=tk.CENTER)
        tree.heading("# 2", text="Departure")
        tree.column("# 3", anchor=tk.CENTER)
        tree.heading("# 3", text="Arrival")
        tree.column("# 4", anchor=tk.CENTER)
        tree.heading("# 4", text="Price")
        tree.column("# 5", anchor=tk.CENTER)
        tree.heading("# 5", text="Available Seats")
        tree.column("# 6", anchor=tk.CENTER)
        tree.heading("# 6", text="")
        tree.bind('<ButtonRelease-1>', self.book_route)

        for i, element in result.iterrows():
            vehicle = vehicle_dataframe.loc[
                vehicle_dataframe['code'] == element['vehicle_code']]
            available_seat = element['seat'].split(';')
            available_time = element['time'].split(';')
            for time in available_time:
                tree.insert('', 'end', values=(
                    vehicle.iloc[0]['name'], time, 'test', element['price'],
                    len(available_seat), "Book Now"))

        self.tree = tree
        tree.pack()

    def book_route(self, event):
        selected = self.tree.item(self.tree.focus())
        

        col = self.tree.identify_column(event.x)
        print('curItem = ', selected)
        print('col = ', col)

        if col == '#0':
            cell_value = selected['text']
        elif col == '#1':
            cell_value = selected['values'][0]
        elif col == '#2':
            cell_value = selected['values'][1]
        elif col == '#3':
            cell_value = selected['values'][2]
        print('cell_value = ', cell_value)
