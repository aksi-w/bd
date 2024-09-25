from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#Таблица Клиентов
class Client(Base):
    __tablename__ = 'client'

    PersonID = Column(Integer, primary_key=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String)

    orders = relationship('Order', back_populates='client')
    carts = relationship('Cart', back_populates='client')

#Таблица заказа
class Order(Base):
    __tablename__ = 'order'

    OrderID = Column(Integer, primary_key=True)
    PersonID = Column(Integer, ForeignKey('client.PersonID'))
    order_date = Column(String)
    delivery_cost = Column(Float)
    payment_type = Column(String)
    status = Column(String)

    client = relationship('Client', back_populates='orders')
    order_items = relationship('OrderProduct', back_populates='order')

#Таблица товара
class Product(Base):
    __tablename__ = 'product'

    ProductID = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    weight = Column(Float)
    description = Column(String)

    order_items = relationship('OrderProduct', back_populates='product')
    cart_items = relationship('CartProduct', back_populates='product')

#Таблица Товар в заказе
class OrderProduct(Base):
    __tablename__ = 'order_product'

    OrderID = Column(Integer, ForeignKey('order.OrderID'), primary_key=True)
    ProductID = Column(Integer, ForeignKey('product.ProductID'), primary_key=True)
    quantity = Column(Integer)

    order = relationship('Order', back_populates='order_items')
    product = relationship('Product', back_populates='order_items')

#Таблица корзины
class Cart(Base):
    __tablename__ = 'cart'

    CartID = Column(Integer, primary_key=True)
    PersonID = Column(Integer, ForeignKey('client.PersonID'))

    client = relationship('Client', back_populates='carts')
    cart_items = relationship('CartProduct', back_populates='cart')

#Таблица товара в корзине
class CartProduct(Base):
    __tablename__ = 'cart_product'

    CartID = Column(Integer, ForeignKey('cart.CartID'), primary_key=True)
    ProductID = Column(Integer, ForeignKey('product.ProductID'), primary_key=True)
    quantity = Column(Integer)

    cart = relationship('Cart', back_populates='cart_items')
    product = relationship('Product', back_populates='cart_items')
