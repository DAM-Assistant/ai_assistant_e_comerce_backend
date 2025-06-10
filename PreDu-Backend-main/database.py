from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import *
import os
from dotenv import load_dotenv

load_dotenv()

# Создаем глобальную переменную engine
engine = create_engine(os.getenv("DB_URL"))

def init_db():
    Base.metadata.create_all(bind=engine)

def create_session():
    Session = sessionmaker(bind=engine)
    return Session()

def get_session():
    session = create_session()
    try:
        yield session
    finally:
        session.close()

init_db()