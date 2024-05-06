from variables import *


def login(username, password):
    if ((user_dataframe[username_header] == username) & (
            user_dataframe[password_header] == password)).any():
        print('Login successful')
    else:
        print('Login failed')


def register(username, password):
    if (user_dataframe[username_header] == username).any():
        print('Username exists')
    else:
        user_dataframe.loc[len(user_dataframe.index)] = [username, password]
        user_dataframe.to_csv(
                '../database/user.csv', mode='w', index=False, header=True)
        print('Registered successfully')
