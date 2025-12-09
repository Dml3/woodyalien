from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class BlogMedia(Base):
    __tablename__ = "blog_media"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)

    post_id = Column(Integer, ForeignKey("blog_posts.id", ondelete="CASCADE"))
    post = relationship("BlogPost", back_populates="media")
