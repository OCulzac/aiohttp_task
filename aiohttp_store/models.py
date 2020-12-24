from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    orders = relationship("Order", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return "<User(last_name='{}', first_name='{}', email={})>"\
                .format(self.last_name, self.first_name, self.email)


class Order(Base):
    __tablename__ = 'Order'

    id = Column(Integer, primary_key=True)
    reg_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="orders")
    order_details = relationship("OrderItem", back_populates="order", cascade="all, delete")

    def __repr__(self):
        return "<Order(reg_date={}, user_id={})>"\
                .format(self.reg_date, self.user_id)


class Book(Base):
    __tablename__ = 'Book'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    author = Column(String(150), nullable=False)
    release_date = Column(String(50), nullable=False)
    order_details = relationship("OrderItem", back_populates="book", cascade="all, delete")

    def __repr__(self):
        return "<Book(name='{}', author='{}', release_date={})>"\
                .format(self.name, self.author, self.release_date)

class Shop(Base):
    __tablename__ = 'Shop'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    address = Column(String(150), nullable=False)
    order_details = relationship("OrderItem", back_populates="shop" , cascade="all, delete")

    def __repr__(self):
        return "<Shop(name='{}', address='{}')>".format(self.name, self.address)

class OrderItem(Base):
    __tablename__ = 'OrderItem'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("Order.id", ondelete="CASCADE"), nullable=False)
    order = relationship("Order", back_populates="order_details")
    book_id = Column(Integer, ForeignKey('Book.id', ondelete="CASCADE"), nullable=False)
    book = relationship("Book", back_populates="order_details")
    shop_id = Column(Integer, ForeignKey('Shop.id', ondelete="CASCADE"), nullable=False)
    shop = relationship("Shop", back_populates="order_details")
    book_quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return "<OrderItem(order_id={}, book_id={}, shop={}, book_quantity={})>"\
                .format(self.order_id, self.book_id, self.shop_id, self.book_quantity)
