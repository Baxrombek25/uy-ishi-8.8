from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from sqlalchemy import DateTime
from datetime import datetime

    
class PaymentStatus(str, enum.Enum):
    paid = "to‘landi"
    pending = "kutmoqda"

class OrderStatus(str, enum.Enum):
    new = "yangi"
    preparing = "tayyorlanmoqda"
    shipped = "jo‘natildi"
    delivered = "yetkazildi"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address = Column(String)
    total_price = Column(Float)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    status = Column(Enum(OrderStatus), default=OrderStatus.new)
    created_at = Column(DateTime, default=datetime.utcnow)
