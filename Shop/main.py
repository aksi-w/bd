from Shop.api import app
from Shop.db import get_session
from Shop.models import Product

def create_products():
    with get_session() as session:
        if session.query(Product).count() > 0:
            print("Товары уже существуют в базе данных.")
            return

        products = [
            Product(name="Футболка", price=500.0, weight=0.3, description="Хлопковая футболка"),
            Product(name="Джинсы", price=2000.0, weight=1.2, description="Классические джинсы"),
            Product(name="Куртка", price=4000.0, weight=1.5, description="Зимняя куртка"),
            Product(name="Кроссовки", price=3000.0, weight=1.0, description="Удобные кроссовки"),
            Product(name="Рубашка", price=1500.0, weight=0.4, description="Классическая рубашка"),
            Product(name="Платье", price=2500.0, weight=0.8, description="Летнее платье"),
            Product(name="Шапка", price=800.0, weight=0.2, description="Теплая шапка"),
            Product(name="Шарф", price=700.0, weight=0.3, description="Уютный шарф"),
            Product(name="Перчатки", price=600.0, weight=0.2, description="Кожаные перчатки"),
            Product(name="Ботинки", price=3500.0, weight=1.4, description="Кожаные ботинки"),
            Product(name="Свитер", price=1800.0, weight=0.6, description="Уютный свитер"),
            Product(name="Шорты", price=1200.0, weight=0.5, description="Летние шорты"),
            Product(name="Пальто", price=5000.0, weight=1.8, description="Осеннее пальто"),
            Product(name="Сандалии", price=1500.0, weight=0.9, description="Летние сандалии"),
            Product(name="Рюкзак", price=3000.0, weight=1.2, description="Прочный рюкзак"),
            Product(name="Часы", price=7000.0, weight=0.15, description="Наручные часы"),
            Product(name="Кошелек", price=1000.0, weight=0.2, description="Кожаный кошелек"),
            Product(name="Бейсболка", price=800.0, weight=0.25, description="Стильная бейсболка"),
            Product(name="Пижама", price=2000.0, weight=0.7, description="Удобная пижама"),
            Product(name="Купальник", price=1200.0, weight=0.3, description="Яркий купальник"),
            Product(name="Очки", price=2500.0, weight=0.1, description="Солнцезащитные очки"),
            Product(name="Ремень", price=1000.0, weight=0.4, description="Кожаный ремень"),
            Product(name="Кепка", price=900.0, weight=0.2, description="Классическая кепка"),
            Product(name="Носки", price=400.0, weight=0.1, description="Хлопковые носки"),
            Product(name="Тапочки", price=700.0, weight=0.5, description="Домашние тапочки"),
            Product(name="Галстук", price=1200.0, weight=0.2, description="Классический галстук"),
            Product(name="Сумка", price=4000.0, weight=1.3, description="Женская сумка"),
            Product(name="Блузка", price=1800.0, weight=0.4, description="Шелковая блузка"),
            Product(name="Юбка", price=2000.0, weight=0.6, description="Короткая юбка"),
            Product(name="Майка", price=600.0, weight=0.2, description="Спортивная майка"),
            Product(name="Брюки", price=2500.0, weight=1.0, description="Классические брюки"),
            Product(name="Кроссовки для бега", price=3500.0, weight=0.9, description="Спортивные кроссовки"),
            Product(name="Толстовка", price=2200.0, weight=0.8, description="Худи с капюшоном"),
            Product(name="Жилет", price=3000.0, weight=1.2, description="Теплый жилет"),
            Product(name="Резиновые сапоги", price=2000.0, weight=1.5, description="Сапоги для дождя"),
            Product(name="Пончо", price=1500.0, weight=0.9, description="Непромокаемое пончо"),
            Product(name="Термобелье", price=1800.0, weight=0.4, description="Зимнее термобелье"),
            Product(name="Шлепанцы", price=700.0, weight=0.3, description="Пляжные шлепанцы"),
            Product(name="Поясная сумка", price=1200.0, weight=0.5, description="Удобная поясная сумка"),
            Product(name="Куртка-дождевик", price=2500.0, weight=1.0, description="Легкая куртка-дождевик")
        ]

        session.bulk_save_objects(products)
        session.commit()
        print("Товары добавлены в базу данных.")


if __name__ == '__main__':
    create_products()
    app.run(debug=True, host="0.0.0.0", port=5000)
