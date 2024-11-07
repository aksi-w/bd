from Shop.api import app
from db import get_session
from models import Person, Order, Product, OrderProduct, Cart, CartProduct
import random

first_names = ["Полина", "Мария", "Дарья", "Наталья", "Александра", "Ольга", "Диана", "Елена", "Альбина", "Юлия"]
middle_names = ["Алексеевна", "Ивановна", "Сергеевна", "Петровна", "Васильевна", "Андреевна", "Михайловна", "Федоровна"]
last_names = ["Пушкина", "Петрова", "Сидорова", "Смирнова", "Кузнецова", "Попова", "Васильева", "Павлова", "Соколова", "Морозова"]
streets = ["Ленина", "Проспект революции", "Гагарина", "Ломоносова", "Лермонтова", "Чехова", "Воли", "Зеленая", "Олимпийская"]

def generate_phone():
    return f"+7-{random.randint(900, 999)}-{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"

def generate_email(first_name, last_name):
    domains = ["mail.com", "yahoo.com", "gmail.com"]
    return f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"

def generate_address():
    return f"ул. {random.choice(streets)}, д. {random.randint(1, 100)}, кв. {random.randint(1, 50)}"

def create_persons(num_persons=10):
    persons = []
    for _ in range(num_persons):
        first_name = random.choice(first_names)
        middle_name = random.choice(middle_names)
        last_name = random.choice(last_names)
        address = generate_address()
        phone = generate_phone()
        email = generate_email(first_name, last_name)
        person = Person(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            address=address,
            phone=phone,
            email=email
        )
        persons.append(person)

    with get_session() as session:
        session.bulk_save_objects(persons)
        session.commit()

product_names = ["Ноутбук", "Смартфон", "Клавиатура", "Мышь", "Монитор", "Принтер", "Наушники", "Флешка", "Зарядное устройство", "Камера"]
descriptions = ["Отличное качество", "Надежный и долговечный", "Современный дизайн", "Высокая производительность", "Компактный и удобный"]

def create_products(num_products=10):
    products = []
    for _ in range(num_products):
        name = random.choice(product_names)
        price = round(random.uniform(100, 5000), 2)
        weight = round(random.uniform(0.1, 10.0), 2)
        description = random.choice(descriptions)
        product = Product(
            name=name,
            price=price,
            weight=weight,
            description=description
        )
        products.append(product)

    with get_session() as session:
        session.bulk_save_objects(products)
        session.commit()

def create_orders(num_orders=10):
    orders = []

    with get_session() as session:
        person_ids = [person.PersonID for person in session.query(Person).all()]

        for _ in range(num_orders):
            person_id = random.choice(person_ids)
            order_date = f"{random.randint(2023, 2024)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
            delivery_cost = round(random.uniform(100, 500), 2)
            payment_type = random.choice(["Наличные", "Карта"])
            status = random.choice(["Обрабатывается", "Отправлено", "Доставлено"])

            order = Order(
                PersonID=person_id,
                order_date=order_date,
                delivery_cost=delivery_cost,
                payment_type=payment_type,
                status=status
            )
            orders.append(order)

        session.bulk_save_objects(orders)
        session.commit()

def create_order_products(num_order_products=10):
    order_products = []

    with get_session() as session:
        order_ids = [order.OrderID for order in session.query(Order).all()]
        product_ids = [product.ProductID for product in session.query(Product).all()]

        existing_combinations = set()

        for _ in range(num_order_products):
            order_id = random.choice(order_ids)
            product_id = random.choice(product_ids)

            if (order_id, product_id) in existing_combinations:
                continue

            quantity = random.randint(1, 5)
            price = session.get(Product, product_id).price

            order_product = OrderProduct(
                OrderID=order_id,
                ProductID=product_id,
                quantity=quantity,
                price=price
            )
            order_products.append(order_product)
            existing_combinations.add((order_id, product_id))

        session.bulk_save_objects(order_products)
        session.commit()

def create_carts(num_carts=10):
    carts = []

    with get_session() as session:
        person_ids = [person.PersonID for person in session.query(Person).all()]
        for _ in range(num_carts):
            person_id = random.choice(person_ids)
            cart = Cart(PersonID=person_id)
            carts.append(cart)

        session.bulk_save_objects(carts)
        session.commit()

def create_cart_products(num_cart_products=10):
    cart_products = []

    with get_session() as session:
        cart_ids = [cart.CartID for cart in session.query(Cart).all()]
        product_ids = [product.ProductID for product in session.query(Product).all()]
        existing_combinations = set()

        for _ in range(num_cart_products):
            cart_id = random.choice(cart_ids)
            product_id = random.choice(product_ids)
            if (cart_id, product_id) in existing_combinations:
                continue

            quantity = random.randint(1, 3)
            cart_product = CartProduct(
                CartID=cart_id,
                ProductID=product_id,
                quantity=quantity
            )
            cart_products.append(cart_product)
            existing_combinations.add((cart_id, product_id))

        session.bulk_save_objects(cart_products)
        session.commit()

create_persons()
create_products()
create_orders()
create_order_products()
create_carts()
create_cart_products()

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
