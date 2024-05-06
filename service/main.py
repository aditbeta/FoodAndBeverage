from tkinter import *
from user import login, register

window = Tk()

width = 340
height = 440


frame = Frame(bg='#333333')

screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
x = int((screenwidth - width) / 2)
y = int((screenheight - height) / 2)

window.title('Sign In')
window.geometry('%dx%d+%d+%d' % (width, height, x, y))
window.configure(bg='#333333')

# Create a label widget
login_label = Label(frame, text='Login')
username_label = Label(frame, text='Username')
username_field = Entry(frame)
password_label = Label(frame, text='Password')
password_field = Entry(frame, show='*')
login_button = Button(frame, text='Login', command=lambda: login(username_field.get(), password_field.get()))
register_button = Button(frame, text='Register', command=lambda: register(username_field.get(), password_field.get()))

# Place the label in the window
login_label.grid(row=0, column=0, columnspan=2)
username_label.grid(row=1, column=0)
username_field.grid(row=1, column=1)
password_label.grid(row=2, column=0)
password_field.grid(row=2, column=1)
login_button.grid(row=3, column=0, columnspan=2)
register_button.grid(row=4, column=0, columnspan=2)

frame.pack()
window.mainloop()
