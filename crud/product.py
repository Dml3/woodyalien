from sqlalchemy.orm import Session
from models.product import Product


def create_product(db: Session, title: str, description: str):
    product = Product(title=title, description=description)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session):
    return db.query(Product).all()


def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if product:
        db.delete(product)
        db.commit()
        return True
    return False
