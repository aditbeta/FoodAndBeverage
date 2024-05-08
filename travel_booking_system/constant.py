import tkinter as tk
from tkinter import ttk

import pandas as pd

blue = '#007afd'
yellow = '#fede00'
red = '#d84f57'
green = '#0bae54'
gray = '#f4f7fe'
white = '#ffffff'
black = '#000000'
font = ('Helvetica', 16)

booking_df = pd.read_csv('data/booking.csv')
location_df = pd.read_csv('data/location.csv')
route_df = pd.read_csv('data/route.csv')
schedule_df = pd.read_csv('data/schedule.csv')
vehicle_df = pd.read_csv('data/vehicle.csv')


def default_result_frame(frame, message):
    label = tk.Label(frame, font=font, text=message)
    label.place(relx=.5, rely=.5, anchor=tk.CENTER)


def default_scroll(frame):
    scroll_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
    scroll_y = tk.Scrollbar(frame, orient=tk.VERTICAL)
    scroll_y.pack(side=tk.RIGHT, fill=tk.X)

    return scroll_x, scroll_y


def default_tree(frame, columns):
    style = ttk.Style()
    style.configure("Treeview.Heading", font=(None, 12))
    style.configure("Treeview", font=(None, 16))
    style.configure('Treeview', rowheight=100)

    scroll_x, scroll_y = default_scroll(frame)
    tree = ttk.Treeview(frame, column=columns, show='headings', height=800,
                        selectmode=tk.NONE,
                        xscrollcommand=scroll_x.set,
                        yscrollcommand=scroll_y.set)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)

    return tree


def df_by_id(df, data_id):
    return df_by_col(df, 'id', data_id)


def df_by_col(df, col, value):
    return df.loc[df[col] == value].iloc[0]
