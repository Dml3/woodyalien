from sqlalchemy.orm import Session
from models.product_media import ProductMedia


def add_media(db: Session, product_id: int, filename: str):
    media = ProductMedia(product_id=product_id, filename=filename)
    db.add(media)
    db.commit()
    db.refresh(media)
    return media


def delete_media(db: Session, media_id: int):
    media = db.query(ProductMedia).filter(ProductMedia.id == media_id).first()
    if media:
        db.delete(media)
        db.commit()
        return True
    return False


def get_media_for_product(db: Session, product_id: int):
    return db.query(ProductMedia).filter(ProductMedia.product_id == product_id).all()
