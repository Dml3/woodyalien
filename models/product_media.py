from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class ProductMedia(Base):
    __tablename__ = "product_media"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)

    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    product = relationship("Product", back_populates="media")
