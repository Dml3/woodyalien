from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text)
    media = Column(JSON, nullable=True)
    date_created = Column(DateTime, default=datetime.utcnow)
