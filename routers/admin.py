import os
import uuid

from fastapi import APIRouter, Request, Depends, Form, File, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from db import SessionLocal
from models.product import Product
from models.product_media import ProductMedia

router = APIRouter(prefix="/admin", tags=["Admin"])
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "static/uploads/products"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def admin_index(request: Request):
    return templates.TemplateResponse("admin/base_admin.html", {"request": request})


@router.get("/products")
def admin_products(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse("admin/admin_products.html", {
        "request": request,
        "products": products
    })


@router.get("/products/create")
def create_product_form(request: Request):
    return templates.TemplateResponse("admin/product_create.html", {"request": request})


@router.post("/products/create")
async def create_product(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    images: list[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    product = Product(title=title, description=description)
    db.add(product)
    db.commit()
    db.refresh(product)

    if images:
        for up in images:
            if not up.filename:
                continue

            ext = up.filename.split(".")[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            path = os.path.join(UPLOAD_DIR, filename)

            with open(path, "wb") as f:
                f.write(await up.read())

            media = ProductMedia(filename=filename, product_id=product.id)
            db.add(media)

        db.commit()

    return RedirectResponse("/admin/products", status_code=303)


@router.get("/products/edit/{product_id}")
def edit_product_form(product_id: int, request: Request, db: Session = Depends(get_db)):
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        return RedirectResponse("/admin/products", status_code=302)

    return templates.TemplateResponse(
        "admin/product_edit.html",
        {"request": request, "product": product}
    )


@router.post("/products/edit/{product_id}")
async def edit_product(
    product_id: int,
    title: str = Form(...),
    description: str = Form(""),
    images: list[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        return RedirectResponse("/admin/products", status_code=302)

    product.title = title
    product.description = description
    db.commit()

    if images:
        for up in images:
            if not up.filename:
                continue

            ext = up.filename.split(".")[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            path = os.path.join(UPLOAD_DIR, filename)

            with open(path, "wb") as f:
                f.write(await up.read())

            media = ProductMedia(filename=filename, product_id=product.id)
            db.add(media)

        db.commit()

    return RedirectResponse(f"/admin/products/edit/{product_id}", status_code=303)


@router.post("/products/{product_id}/media/{media_id}/delete")
def delete_media(product_id: int, media_id: int, db: Session = Depends(get_db)):
    media = db.query(ProductMedia).filter_by(id=media_id, product_id=product_id).first()

    if media:
        filepath = os.path.join(UPLOAD_DIR, media.filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass

        db.delete(media)
        db.commit()

    return RedirectResponse(f"/admin/products/edit/{product_id}", status_code=303)


@router.post("/products/{product_id}/delete")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter_by(id=product_id).first()

    if not product:
        return RedirectResponse("/admin/products", status_code=302)

    for m in product.media:
        filepath = os.path.join(UPLOAD_DIR, m.filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass

    db.delete(product)
    db.commit()

    return RedirectResponse("/admin/products", status_code=303)
