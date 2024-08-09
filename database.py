from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///user_data.db'

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class UserHistory(Base):
    __tablename__ = 'user_history'
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, nullable=False, unique=True)
    query = Column(Text, nullable=True)
    response = Column(Text, nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def store_user_history(phone_number, query, response):
    with SessionLocal() as session:
        existing_entry = session.query(UserHistory).filter(UserHistory.phone_number == phone_number).first()
        if existing_entry:
            # Append new data to existing query and response
            existing_entry.query = f"{existing_entry.query or ''}\n{query}"
            existing_entry.response = f"{existing_entry.response or ''}\n{response}"
        else:
            session.add(UserHistory(
                phone_number=phone_number,
                query=query,
                response=response
            ))
        session.commit()

def phone_number_exists(phone_number):
    with SessionLocal() as session:
        exists = session.query(UserHistory).filter(UserHistory.phone_number == phone_number).first() is not None
    return exists

def add_phone_number(phone_number):
    with SessionLocal() as session:
        if not session.query(UserHistory).filter(UserHistory.phone_number == phone_number).first():
            session.add(UserHistory(
                phone_number=phone_number,
                query='',
                response=''
            ))
            session.commit()

def get_user_history(phone_number):
    with SessionLocal() as session:
        results = session.query(UserHistory).filter(UserHistory.phone_number == phone_number).all()
        history = []
        for r in results:
            # Split queries and responses if they are concatenated in a single entry
            queries = [q for q in r.query.split('\n') if q.strip()] if r.query else []
            responses = [a for a in r.response.split('\n') if a.strip()] if r.response else []
            
            # Combine them into a list of dictionaries for easy display
            for q, a in zip(queries, responses):
                if q and a:  # Ensure neither the question nor the answer is empty
                    history.append({'query': q, 'response': a})
        return history