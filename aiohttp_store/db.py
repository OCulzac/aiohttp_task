from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date,
)

meta = MetaData()

users = Table(
    'users', meta,

    Column('id', Integer, primary_key=True),
    Column('last_name', String(50), nullable=False),
    Column('first_name', String(50), nullable=False),
    Column('email', String(50), nullable=False)
)

orders = Table(
    'orders', meta,

    Column('id', Integer, primary_key=True),
    Column('reg_date', Date, nullable=False),
    Column('user_id', Integer, ForeignKey("users.id"), nullable=False)
)

shops = Table(
    'shops', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('address', String(150), nullable=False)
)

books = Table(
    'books', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('author', String(50), nullable=False),
    Column('release_date', Date, nullable=False)
)

orderitem = Table(
    'orderitem', meta,
    Column('id', Integer, primary_key=True),
    Column('order_id', Integer, ForeignKey("orders.id"), nullable=False),
    Column('book_id', Integer, ForeignKey("books.id"), nullable=False),
    Column('shop_id', Integer, ForeignKey("shops.id"), nullable=False),
    Column('book_quantity', Integer, nullable=False)
)


