from sqlalchemy import create_engine, Column, DateTime, Float, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

from dotenv import load_dotenv
import os

# Loading env vars
load_dotenv('.env')
TARGET_DB_URL = os.getenv("TARGET_DB_URL")

engine = create_engine(TARGET_DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Trigger(Base):
    __tablename__ = 'trigger'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    date = Column(DateTime)
    origin = Column(String)
    
    signals = relationship("Signal", back_populates="trigger")

class Signal(Base):
    __tablename__ = 'signal'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    data = Column(String)
    timestamp = Column(DateTime)
    signal_id = Column(Integer, ForeignKey('trigger.id'))
    value = Column(Float)
    
    trigger = relationship("Trigger", back_populates="signals")

def init_db():
    Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()