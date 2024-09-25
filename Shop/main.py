from db import session
from models import Client, Order, Product, OrderProduct, Cart, CartProduct

# Пример добавления клиента
new_client = Client(first_name='Ivan', middle_name='Ivanovich', last_name='Ivanov', address='123 Main St', phone='123456789', email='ivanov@example.com')
session.add(new_client)
session.commit()

# Вывод всех клиентов
clients = session.query(Client).all()
for client in clients:
    print(f'{client.first_name} {client.last_name}')
