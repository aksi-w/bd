from faker import Faker
from db import session
from models import Person

fake = Faker()

def create_persons(num_persons=1000):
    persons = []

    for i in range(num_persons):
        first_name = fake.first_name()
        middle_name = fake.first_name()
        last_name = fake.last_name()
        address = fake.address()
        phone = fake.phone_number()
        email = fake.email()
        person = Person(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            address=address,
            phone=phone,
            email=email
        )
        persons.append(person)
    session.bulk_save_objects(persons)
    session.commit()
create_persons(1000)

persons = session.query(Person).all()
for person in persons[:3]:  # проверяю, что они вообще сгенерировалиь
    print(f'{person.first_name} {person.last_name}')
