from book import Book
from order import Order
from login import Login


def book_page(main_frame, user_id):
    Book(main_frame, user_id)

def order_page(main_frame, user_id):
    Order(main_frame, user_id)

def login_page(main_frame, user_id):
    Login(main_frame)
