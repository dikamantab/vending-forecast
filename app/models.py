from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

# class Temperature(Base):
#     __tablename__ = "environment_data"
#     id = Column(Integer, primary_key=True, index=True)
#     machine_id = Column(String(100), index=True, nullable=True)
#     temperature = Column(Float)
#     humidity = Column(Float, nullable=True)
#     timestamp = Column(DateTime, index=True)

class VendingSale(Base):
    __tablename__ = "vending_sales"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(50), unique=True, index=True, nullable=False)
    vm_code = Column(String(50), index=True, nullable=False)
    product_name = Column(String(255), nullable=False)
    sku = Column(String(50), index=True, nullable=False)
    slot = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    gross = Column(Integer, nullable=False)
    payment_method = Column(String(50), nullable=False)
    transaction_time = Column(DateTime, nullable=False)