from app.models.base import Base
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column

class Product(Base):
    __tablename__ = 'product'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(100), nullable=False)
    price = mapped_column(Integer, nullable=False)
    description = mapped_column(Text, nullable=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f'<Product id={self.id}, name={self.name}, price={self.price}>'
