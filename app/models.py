from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class Temperature(Base):
    __tablename__ = "environment_data"
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, index=True, nullable=True)
    temperature = Column(Float)
    humidity = Column(Float, nullable=True)
    timestamp = Column(DateTime, index=True)

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, index=True)
    product = Column(String)
    qty = Column(Integer)
    timestamp = Column(DateTime, index=True)