import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

import pandas as pd
import os

blue = '#007afd'
yellow = '#fede00'
red = '#d84f57'
green = '#0bae54'
gray = '#f4f7fe'
white = '#ffffff'
black = '#000000'
font1 = ('Helvetica', 18)
font2 = ('Helvetica', 16)
width = 1280
height = 720


def full_path(path):
    return os.path.join(os.path.dirname(__file__), path)


def read_csv(path):
    return pd.read_csv(full_path(path))


booking_df = read_csv('data/booking.csv')
location_df = read_csv('data/location.csv')
route_df = read_csv('data/route.csv')
schedule_df = read_csv('data/schedule.csv')
vehicle_df = read_csv('data/vehicle.csv')
order_df = read_csv('data/order.csv')


def default_result_frame(frame, message):
    label = tk.Label(frame, font=font2, text=message)
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


def df_val(df, col):
    return df.iloc[0][col]


def write_append(path, df, values):
    last_id = len(df.index)
    values[0] = last_id + 1
    df.loc[last_id] = values
    df.to_csv(full_path(path), mode='w', index=False, header=True)
    return last_id + 1


def write_update(path, df, index, col, value):
    df.loc[index, col] = value
    df.to_csv(full_path(path), index=False, header=True)


def delete_pages(parent):
    for frame in parent.winfo_children():
        frame.destroy()


def popup_showinfo(title, message):
    showinfo(title, message)
