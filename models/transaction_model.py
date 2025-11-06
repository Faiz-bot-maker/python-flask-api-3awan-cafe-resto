from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from config.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menus.menu_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relasi ke menu
    menu = relationship("Menu", backref="transactions")

    def to_dict(self):
        return {
            "id": self.id,
            "menu_id": self.menu_id,
            "quantity": self.quantity,
            "total_price": float(self.total_price),
            "payment_method": self.payment_method,
            "created_at": str(self.created_at)
        }
