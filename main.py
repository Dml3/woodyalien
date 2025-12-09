from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from db import SessionLocal, engine, Base
from models.product import Product
from models.product_media import ProductMedia

from routers import admin, blog
from api import products_api

app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "products": products,
            "active_page": "index",
        }
    )


app.include_router(admin.router)
app.include_router(products_api.router)
app.include_router(blog.router)
