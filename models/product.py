from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    media = relationship(
        "ProductMedia",
        back_populates="product",
        cascade="all, delete-orphan"
    )
