from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Создание подключения к базе данных
engine = create_engine('sqlite:///:memory:', echo=True)

# Создание всех таблиц в базе данных
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
