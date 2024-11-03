from flask import Flask, request, jsonify
from Shop.models import Person, Order, Product, OrderProduct, Cart, CartProduct
from Shop.db import get_session

app = Flask(__name__)

# Получить всех пользователей
@app.route('/persons', methods=['GET'])
def get_persons():
    with get_session() as session:
        persons = session.query(Person).all()
        return jsonify([{"PersonID": p.PersonID, "first_name": p.first_name, "last_name": p.last_name} for p in persons])

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
        return jsonify({"message": "Person added", "PersonID": new_person.PersonID}), 201

@app.route('/persons/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    data = request.json
    with get_session() as session:
        person = session.query(Person).get(person_id)
        if not person:
            return jsonify({"message": "Person not found"}), 404

        person.first_name = data.get('first_name', person.first_name)
        person.middle_name = data.get('middle_name', person.middle_name)
        person.last_name = data.get('last_name', person.last_name)
        person.address = data.get('address', person.address)
        person.phone = data.get('phone', person.phone)
        person.email = data.get('email', person.email)

        session.commit()
        return jsonify({"message": "Person updated"})

@app.route('/persons/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    with get_session() as session:
        person = session.query(Person).get(person_id)
        if not person:
            return jsonify({"message": "Person not found"}), 404
        session.delete(person)
        session.commit()
        return jsonify({"message": "Person deleted"})

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API is working"}), 200

