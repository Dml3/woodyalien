from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=True, unique=True)
    excerpt = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    date_create = Column(DateTime, default=datetime.utcnow)
    date_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    media = relationship(
        "BlogMedia",
        back_populates="post",
        cascade="all, delete-orphan",
        order_by="BlogMedia.id"
    )
