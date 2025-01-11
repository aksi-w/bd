from datetime import datetime

from flask import Flask, request, jsonify, render_template, url_for, redirect
from Shop.models import Person, Product, Cart, CartProduct, OrderProduct, Order
from Shop.db import get_session
from flask import session
from math import ceil

app = Flask(__name__, template_folder='../templates')
app.secret_key = 'lalalalalalalalalallala'


@app.before_request
def override_method():
    if request.method == 'POST' and '_method' in request.form:
        request.environ['REQUEST_METHOD'] = request.form['_method'].upper()


@app.route('/')
def home():
    user_id = session.get('user_id')
    page = request.args.get('page', 1, type=int)
    per_page = 15
    offset = (page - 1) * per_page
    with get_session() as db_session:
        products = db_session.query(Product).limit(per_page).offset(offset).all()
        total = db_session.query(Product).count()
        pages = ceil(total / per_page)

        if user_id:
            person = db_session.query(Person).get(user_id)
            cart = db_session.query(Cart).filter_by(PersonID=user_id).first()
            cart_items = []
            if cart:
                cart_products = db_session.query(CartProduct).filter_by(CartID=cart.CartID).all()
                for cp in cart_products:
                    product = db_session.query(Product).get(cp.ProductID)
                    if product:
                        cart_items.append({
                            "name": product.name,
                            "quantity": cp.quantity,
                            "price": product.price * cp.quantity,
                            "ProductID": cp.ProductID
                        })
            return render_template('web.html', products=products, person=person, cart_items=cart_items, page=page,
                                   pages=pages)
        return render_template('web.html', products=products, page=page, pages=pages)



@app.route('/products', methods=['GET'])
def get_products():
    with get_session() as session:
        products = session.query(Product).all()
        return jsonify([{
            "ProductID": p.ProductID,
            "name": p.name,
            "price": p.price,
            "weight": p.weight,
            "description": p.description
        } for p in products])


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


@app.route('/cart/<int:person_id>')
def show_cart(person_id):
    user_id = session.get('user_id')
    with get_session() as db_session:
        if user_id:
            cart = db_session.query(Cart).filter_by(PersonID=user_id).first()
            if not cart:
                cart = Cart(PersonID=user_id)
                db_session.add(cart)
                db_session.commit()
            cart_products = db_session.query(CartProduct).filter_by(CartID=cart.CartID).all()
        else:
            cart_products = session.get('temp_cart', {}).items()

        cart_items = []
        for cp in cart_products:
            if user_id:
                product_id = cp.ProductID
                quantity = cp.quantity
            else:
                product_id, quantity = cp
            product = db_session.query(Product).get(product_id)
            if product:
                cart_items.append({
                    "name": product.name,
                    "quantity": quantity,
                    "price": product.price * quantity,
                    "ProductID": product.ProductID
                })

        person = db_session.query(Person).get(user_id) if user_id else None
        return render_template('cart.html', cart_items=cart_items, person=person, person_id=person_id)


@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    user_id = session.get('user_id')
    with get_session() as db_session:
        try:
            if user_id:
                cart = db_session.query(Cart).filter_by(PersonID=user_id).first()
                if not cart:
                    cart = Cart(PersonID=user_id)
                    db_session.add(cart)
                    db_session.commit()
                cart_product = db_session.query(CartProduct).filter_by(
                    CartID=cart.CartID,
                    ProductID=data['ProductID']
                ).first()
                if cart_product:
                    cart_product.quantity += data.get('quantity', 1)
                else:
                    cart_product = CartProduct(
                        CartID=cart.CartID,
                        ProductID=data['ProductID'],
                        quantity=data.get('quantity', 1)
                    )
                    db_session.add(cart_product)
                db_session.commit()
            else:
                temp_cart = session.get('temp_cart', {})
                product_id = data['ProductID']
                quantity = data.get('quantity', 1)
                if product_id in temp_cart:
                    temp_cart[product_id] += quantity
                else:
                    temp_cart[product_id] = quantity
                session['temp_cart'] = temp_cart
            return jsonify({"message": "Товар добавлен в корзину"}), 201
        except Exception as e:
            db_session.rollback()
            return jsonify({"message": str(e)}), 500


@app.route('/cart/<int:product_id>', methods=['DELETE'])
def delete_from_cart(product_id):
    user_id = session.get('user_id')
    with get_session() as db_session:
        try:
            if user_id:
                cart = db_session.query(Cart).filter_by(PersonID=user_id).first()
                if not cart:
                    return jsonify({"message": "Корзина пуста"}), 404

                cart_product = db_session.query(CartProduct).filter_by(
                    CartID=cart.CartID,
                    ProductID=product_id
                ).first()

                if not cart_product:
                    return jsonify({"message": "Товар в корзине не найден"}), 404

                db_session.delete(cart_product)
                db_session.commit()
            else:
                temp_cart = session.get('temp_cart', {})
                if product_id in temp_cart:
                    del temp_cart[product_id]
                    session['temp_cart'] = temp_cart
                else:
                    return jsonify({"message": "Товар в корзине не найден"}), 404
            return jsonify({"message": "Товар удален из корзины"}), 200
        except Exception as e:
            db_session.rollback()
            return jsonify({"message": str(e)}), 500


@app.route('/cart/clear', methods=['DELETE'])
def clear_cart():
    user_id = session.get('user_id')
    with get_session() as db_session:
        try:
            if user_id:
                cart = db_session.query(Cart).filter_by(PersonID=user_id).first()
                if not cart:
                    return jsonify({"message": "Корзина пуста"}), 404

                db_session.query(CartProduct).filter_by(CartID=cart.CartID).delete()
                db_session.commit()
            else:
                session.pop('temp_cart', None)
            return jsonify({"message": "Корзина очищена"}), 200
        except Exception as e:
            db_session.rollback()
            return jsonify({"message": str(e)}), 500


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
        return jsonify({"message": "Пользователь создан", "PersonID": new_person.PersonID}), 201


@app.route('/persons/<int:person_id>', methods=['GET'])
def get_person(person_id):
    with get_session() as session:
        person = session.query(Person).get(person_id)
        if not person:
            return jsonify({"message": "Пользователь не найден"}), 404

        return jsonify({
            "PersonID": person.PersonID,
            "first_name": person.first_name,
            "middle_name": person.middle_name,
            "last_name": person.last_name,
            "address": person.address,
            "phone": person.phone,
            "email": person.email
        })


@app.route('/cart/<int:person_id>', methods=['GET'])
def view_cart(person_id):
    with get_session() as session:
        cart = session.query(Cart).filter_by(PersonID=person_id).first()
        if not cart:
            return render_template('cart.html', cart_items=[])

        cart_products = session.query(CartProduct).filter_by(CartID=cart.CartID).all()
        cart_items = []
        for cp in cart_products:
            product = session.query(Product).get(cp.ProductID)
            if product:
                cart_items.append({
                    "ProductID": product.ProductID,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "quantity": cp.quantity,
                    "total_price": product.price * cp.quantity
                })
        return render_template('cart.html', cart_items=cart_items)


@app.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data.get('email')
    with get_session() as db_session:
        try:
            person = db_session.query(Person).filter_by(email=email).first()
            if person:
                session['user_id'] = person.PersonID
                temp_cart = session.get('temp_cart', {})
                if temp_cart:
                    cart = db_session.query(Cart).filter_by(PersonID=person.PersonID).first()
                    if not cart:
                        cart = Cart(PersonID=person.PersonID)
                        db_session.add(cart)
                        db_session.commit()
                    for product_id, quantity in temp_cart.items():
                        cart_product = db_session.query(CartProduct).filter_by(
                            CartID=cart.CartID,
                            ProductID=product_id
                        ).first()
                        if cart_product:
                            cart_product.quantity += quantity
                        else:
                            cart_product = CartProduct(
                                CartID=cart.CartID,
                                ProductID=product_id,
                                quantity=quantity
                            )
                            db_session.add(cart_product)
                    db_session.commit()
                    session.pop('temp_cart', None)
                return redirect(url_for('show_cart', person_id=person.PersonID))
            else:
                new_person = Person(
                    first_name=data['first_name'],
                    middle_name=data.get('middle_name'),
                    last_name=data['last_name'],
                    address=data['address'],
                    phone=data['phone'],
                    email=data['email']
                )
                db_session.add(new_person)
                db_session.commit()
                session['user_id'] = new_person.PersonID
                return redirect(url_for('show_cart', person_id=new_person.PersonID))
        except Exception as e:
            db_session.rollback()
            return jsonify({"message": str(e)}), 500


@app.route('/logout', methods=['POST'])
def logout():
    user_id = session.pop('user_id', None)
    if user_id:
        with get_session() as db_session:
            try:
                cart = db_session.query(Cart).filter_by(PersonID=user_id).first()
                if cart:
                    db_session.query(CartProduct).filter_by(CartID=cart.CartID).delete()
                    db_session.commit()
            except Exception as e:
                db_session.rollback()
                return jsonify({"message": str(e)}), 500
    return redirect(url_for('home'))


@app.route('/order', methods=['POST'])
def place_order():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Пользователь не авторизован"}), 401

    data = request.form
    with get_session() as db_session:
        try:
            person = db_session.query(Person).get(user_id)
            if not person:
                return jsonify({"message": "Пользователь не найден"}), 404

            # Проверка данных заказа
            delivery_cost = data.get('delivery_cost', 0)
            payment_type = data.get('payment_type')
            if not payment_type:
                return jsonify({"message": "Не указан тип оплаты"}), 400
            order = Order(
                PersonID=person.PersonID,
                order_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                delivery_cost=delivery_cost,
                payment_type=payment_type,
                status='Ожидает оплаты'
            )
            db_session.add(order)
            db_session.commit()
            cart = db_session.query(Cart).filter_by(PersonID=user_id).first()
            if not cart:
                return jsonify({"message": "Корзина пуста"}), 400

            cart_products = db_session.query(CartProduct).filter_by(CartID=cart.CartID).all()
            if not cart_products:
                return jsonify({"message": "Корзина пуста"}), 400

            # Добавление товаров из корзины в заказ
            for cp in cart_products:
                product = db_session.query(Product).get(cp.ProductID)
                if not product:
                    return jsonify({"message": f"Товар с ID {cp.ProductID} не найден"}), 400

                order_product = OrderProduct(
                    OrderID=order.OrderID,
                    ProductID=cp.ProductID,
                    quantity=cp.quantity,
                    price=product.price
                )
                db_session.add(order_product)
            db_session.query(CartProduct).filter_by(CartID=cart.CartID).delete()
            db_session.commit()

            return jsonify({"message": "Заказ успешно оформлен", "OrderID": order.OrderID}), 201

        except Exception as e:
            db_session.rollback()
            return jsonify({"message": f"Произошла ошибка: {str(e)}"}), 500


@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    with get_session() as session:
        new_product = Product(
            name=data['name'],
            price=data['price'],
            weight=data['weight'],
            description=data['description']
        )
        session.add(new_product)
        session.commit()
        return jsonify({"message": "Товар создан", "ProductID": new_product.ProductID}), 201


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    with get_session() as session:
        product = session.query(Product).get(product_id)
        if not product:
            return jsonify({"message": "Товар не найден"}), 404
        product.name = data['name']
        product.price = data['price']
        product.weight = data['weight']
        product.description = data['description']
        session.commit()
        return jsonify({"message": "Товар обновлен"}), 200


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    with get_session() as session:
        product = session.query(Product).get(product_id)
        if not product:
            return jsonify({"message": "Товар не найден"}), 404
        session.delete(product)
        session.commit()
        return jsonify({"message": "Товар удален"}), 200

@app.route('/admin')
def admin():
    return render_template('admin.html')
