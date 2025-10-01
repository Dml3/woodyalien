from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from db import SessionLocal, init_db, Product

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse("index.html", {"request": request, "products": products, "active_page": "index"})


@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "active_page": "about"})


@app.get("/blog")
def blog(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request, "active_page": "blog"})


@app.get("/shop")
def shop(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse("shop.html", {"request": request, "products": products, "active_page": "shop"})


@app.get("/shop/{product_id}")
def product_page(product_id: int, request: Request, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    return templates.TemplateResponse("product.html", {"request": request, "product": product, "active_page": "shop"})
