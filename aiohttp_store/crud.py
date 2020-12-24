from sqlalchemy import create_engine
from .settings import config
from sqlalchemy.orm import sessionmaker
from .models import Base, Order, User, Book, Shop, OrderItem

from contextlib import contextmanager
import yaml
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent

books_path = BASE_DIR / 'aiohttp_store' / 'books.yaml'
shop_path = BASE_DIR / 'aiohttp_store' / 'shop.yaml'
orderdetail_path = BASE_DIR / 'aiohttp_store' / 'orderdetails.yaml'
users_path = BASE_DIR / 'aiohttp_store' / 'users.yaml'
order_path = BASE_DIR / 'aiohttp_store' / 'orders.yaml'

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
db_url = DSN.format(**config['postgres'])

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Session manager func


    """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def recreate_database():
    """db creation func


    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def load_yaml():
    """ upload preloaded data into db func


    """
    with session_scope() as s:
        for data in yaml.load_all(open(books_path), Loader=yaml.FullLoader):
            book = Book(**data)
            s.add(book)

    with session_scope() as s:
        for data in yaml.load_all(open(users_path), Loader=yaml.FullLoader):
            user = User(**data)
            s.add(user)

    with session_scope() as s:
        for data in yaml.load_all(open(shop_path), Loader=yaml.FullLoader):
            shop = Shop(**data)
            s.add(shop)

    with session_scope() as s:
        for data in yaml.load_all(open(order_path), Loader=yaml.FullLoader):
            order = Order(**data)
            s.add(order)

    with session_scope() as s:
        for data in yaml.load_all(open(orderdetail_path), Loader=yaml.FullLoader):
            orderdetail = OrderItem(**data)
            s.add(orderdetail)


if __name__ == '__main__':
    recreate_database()

    load_yaml()

    with session_scope() as s:
        r = s.query(User).filter_by(last_name='Doe').first()
        print("filter_by:", r)

        r = s.query(User).filter_by(last_name='Chinaman').all()
        print("filter_by:", r)
