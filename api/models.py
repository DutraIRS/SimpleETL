from sqlalchemy import create_engine, Column, DateTime, Float
from sqlalchemy.orm import declarative_base, sessionmaker

from dotenv import load_dotenv
import os

# Loading env vars
load_dotenv('.env')
SOURCE_DB_URL = os.getenv("SOURCE_DB_URL")

engine = create_engine(SOURCE_DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Data(Base):
    __tablename__ = 'data'
    
    timestamp = Column(DateTime, primary_key=True)
    wind_speed = Column(Float)
    power = Column(Float)
    ambient_temperature = Column(Float)

def init_db():
    Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()