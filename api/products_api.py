from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import SessionLocal
from models.product import Product
from models.product_media import ProductMedia
from schemas.product import ProductCreate, ProductOut


router = APIRouter(prefix="/api/products", tags=["Products API"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[ProductOut])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")
    return product


@router.post("/", response_model=ProductOut)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    product = Product(title=data.title, description=data.description)
    db.add(product)
    db.commit()
    db.refresh(product)

    for filename in data.media:
        media = ProductMedia(filename=filename, product_id=product.id)
        db.add(media)

    db.commit()
    db.refresh(product)
    return product
