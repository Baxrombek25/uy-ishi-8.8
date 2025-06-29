from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    discount = Column(Float, default=0)
    stock = Column(Integer)
    image = Column(String, nullable=True)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category")
