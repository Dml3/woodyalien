from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import json

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    images = Column(Text, nullable=True)  # JSON список

    def get_images(self):
        return json.loads(self.images) if self.images else []


engine = create_engine("sqlite:///./woodyalien.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Product).count() == 0:
        db.add_all([
            Product(
                name="Инопланетные часы",
                description="Стильнаые часы для вашего дома",
                images=json.dumps(["clock1.jpg", "clock2.jpg"])
            ),
            Product(
                name="Космический подсвечник",
                description="Уютный подсвечник из другой галактики",
                images=json.dumps(["candlestick1.jpg", "candlestick2.jpg", "candlestick3.jpg"])
            ),
            Product(
                name="Галактическая ваза",
                description="Украшение для стола и полки",
                images=json.dumps(["vase.jpg"])
            )
        ])
        db.commit()
    db.close()
