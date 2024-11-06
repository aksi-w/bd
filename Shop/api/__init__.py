from flask import Flask, request, jsonify
from Shop.models import Person, Order, Product, OrderProduct, Cart, CartProduct
from Shop.db import get_session

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API работает"}), 200


@app.route('/persons', methods=['GET'])
def get_persons():
    with get_session() as session:
        persons = session.query(Person).all()
        return jsonify(
            [{"PersonID": p.PersonID, "first_name": p.first_name, "last_name": p.last_name, "address": p.address,
              "phone": p.phone, "email": p.email} for p in persons])


@app.route('/persons/<int:person_id>', methods=['GET'])
def get_person_by_id(person_id):
    with get_session() as session:
        person = session.query(Person).get(person_id)
        if not person:
            return jsonify({"message": "Пользователь с такими данными не найден"}), 404

        return jsonify({
            "PersonID": person.PersonID,
            "first_name": person.first_name,
            "middle_name": person.middle_name,
            "last_name": person.last_name,
            "address": person.address,
            "phone": person.phone,
            "email": person.email
        })


@app.route('/persons', methods=['POST'])
def add_person():
    data = request.json
    with get_session() as session:
        new_person = Person(
            first_name=data['first_name'],
            middle_name=data.get('middle_name'),
            last_name=data['last_name'],
            address=data['address'],
            phone=data['phone'],
            email=data['email']
        )
        session.add(new_person)
        session.commit()
        return jsonify({"message": "Пользователь добавлен", "PersonID": new_person.PersonID}), 201


@app.route('/persons/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    data = request.json
    with get_session() as session:
        person = session.query(Person).get(person_id)
        if not person:
            return jsonify({"message": "Пользователь не найден"}), 404

        person.first_name = data.get('first_name', person.first_name)
        person.middle_name = data.get('middle_name', person.middle_name)
        person.last_name = data.get('last_name', person.last_name)
        person.address = data.get('address', person.address)
        person.phone = data.get('phone', person.phone)
        person.email = data.get('email', person.email)

        session.commit()
        return jsonify({"message": "Данные пользователя обновлены"})


@app.route('/persons/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    with get_session() as session:
        person = session.query(Person).get(person_id)
        if not person:
            return jsonify({"message": "Пользователь не найден"}), 404
        session.delete(person)
        session.commit()
        return jsonify({"message": "Пользователь удален"})


@app.route('/products', methods=['GET'])
def get_products():
    with get_session() as session:
        products = session.query(Product).all()
        return jsonify([{"ProductID": p.ProductID, "name": p.name, "price": p.price, "weight": p.weight,
                         "description": p.description} for p in products])


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    with get_session() as session:
        product = session.query(Product).get(product_id)
        if not product:
            return jsonify({"message": "Товар не найден"}), 404

        return jsonify({
            "ProductID": product.ProductID,
            "name": product.name,
            "price": product.price,
            "weight": product.weight,
            "description": product.description
        })


@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    with get_session() as session:
        new_product = Product(
            name=data['name'],
            price=data['price'],
            weight=data['weight'],
            description=data.get('description', '')
        )
        session.add(new_product)
        session.commit()
        return jsonify({"message": "Товар добавлен", "ProductID": new_product.ProductID}), 201


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    with get_session() as session:
        product = session.query(Product).get(product_id)
        if not product:
            return jsonify({"message": "Товар не найден"}), 404

        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.weight = data.get('weight', product.weight)
        product.description = data.get('description', product.description)

        session.commit()
        return jsonify({"message": "Данные товара обновлены"})


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    with get_session() as session:
        product = session.query(Product).get(product_id)
        if not product:
            return jsonify({"message": "Товар не найден"}), 404
        session.delete(product)
        session.commit()
        return jsonify({"message": "Товар удален"})


@app.route('/orders', methods=['GET'])
def get_orders():
    with get_session() as session:
        orders = session.query(Order).all()
        return jsonify([{
            "OrderID": o.OrderID,
            "PersonID": o.PersonID,
            "order_date": o.order_date,
            "delivery_cost": o.delivery_cost,
            "payment_type": o.payment_type,
            "status": o.status
        } for o in orders])


@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    with get_session() as session:
        order = session.query(Order).get(order_id)
        if not order:
            return jsonify({"message": "Заказ не найден"}), 404
        session.delete(order)
        session.commit()
        return jsonify({"message": "Заказ удален"})


@app.route('/order_products', methods=['GET'])
def get_order_products():
    with get_session() as session:
        order_products = session.query(OrderProduct).all()
        return jsonify([{
            "OrderID": op.OrderID,
            "ProductID": op.ProductID,
            "quantity": op.quantity,
            "price": op.price
        } for op in order_products])


@app.route('/order_products/<int:order_id>/<int:product_id>', methods=['DELETE'])
def delete_order_product(order_id, product_id):
    with get_session() as session:
        order_product = session.query(OrderProduct).get((order_id, product_id))
        if not order_product:
            return jsonify({"message": "Товар отсутствует в заказе"}), 404
        session.delete(order_product)
        session.commit()
        return jsonify({"message": "Товар удален из заказа"})


@app.route('/carts', methods=['GET'])
def get_carts():
    with get_session() as session:
        carts = session.query(Cart).all()
        return jsonify([{
            "CartID": c.CartID,
            "PersonID": c.PersonID
        } for c in carts])


@app.route('/carts/<int:cart_id>', methods=['DELETE'])
def delete_cart(cart_id):
    with get_session() as session:
        cart = session.query(Cart).get(cart_id)
        if not cart:
            return jsonify({"message": "Cart not found"}), 404
        session.delete(cart)
        session.commit()
        return jsonify({"message": "Данные о корзине не найдены"})


@app.route('/cart_products', methods=['GET'])
def get_cart_products():
    with get_session() as session:
        cart_products = session.query(CartProduct).all()
        return jsonify([{
            "CartID": cp.CartID,
            "ProductID": cp.ProductID,
            "quantity": cp.quantity
        } for cp in cart_products])


@app.route('/cart_products/<int:cart_id>/<int:product_id>', methods=['DELETE'])
def delete_cart_product(cart_id, product_id):
    with get_session() as session:
        cart_product = session.query(CartProduct).get((cart_id, product_id))
        if not cart_product:
            return jsonify({"message": "Товар в корзине не найден"}), 404
        session.delete(cart_product)
        session.commit()
        return jsonify({"message": "Товар удален из корзины"})
