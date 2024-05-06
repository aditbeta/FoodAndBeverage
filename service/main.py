from tkinter import *
import pandas as pd

window = Tk()

width = 340
height = 440


user = pd.read_csv('../database/user.csv')


def login():
    if ((user['username'] == username_field.get()) & (user['password'] == password_field.get())).any():
        print('Login successful')
    else:
        print('Login failed')


def register():
    if (user['username'] == username_field.get()).any():
        print('Username exists')
    else:
        new_user = {'username': username_field.get(), 'password': password_field.get()}
        user.loc[len(user.index)] = [username_field.get(), password_field.get()]
        user.to_csv('../database/user.csv', mode='w', index=False, header=True)
        print('Registered successfully')


frame = Frame(bg='#333333')

screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
#
#
# width = 800
# height = 600
x = int((screenwidth - width) / 2)
y = int((screenheight - height) / 2)
#
# window.resizable(True, True)
# window.geometry('%dx%d+%d+%d' % (width, height, x, y))
# window.title('Coffee & Eatery Self Service')
# window.mainloop()


window.title('Sign In')
window.geometry('%dx%d+%d+%d' % (width, height, x, y))
window.configure(bg='#333333')

# label = Label(window, text='Sign In')
# label.pack()

# Create a label widget
login_label = Label(frame, text='Login')
username_label = Label(frame, text='Username')
username_field = Entry(frame)
password_label = Label(frame, text='Password')
password_field = Entry(frame, show='*')
login_button = Button(frame, text='Login', command=login)
register_button = Button(frame, text='Register', command=register)

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
