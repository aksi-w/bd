# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine('sqlite:///shop.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    session = Session()
    return session
