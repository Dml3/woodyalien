from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Подключаем папку с шаблонами
templates = Jinja2Templates(directory="templates")

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Пример продукта (можно заменить на данные из базы)
products = [
    {"name": "Инопланетная лампа", "image": ["clock1.jpg", "clock2.jpg"], "description": "Стильная лампа для вашего дома"},
    {"name": "Космическое кресло", "image": ["candlestick1.jpg", "candlestick2.jpg", "candlestick3.jpg"], "description": "Комфортное кресло из другой галактики"},
    {"name": "Галактическая ваза", "image": ["sculpture1.jpg"], "description": "Украшение для стола и полки"}
]

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "products": products,
            "active_page": "index"  # для подсветки меню
        }
    )
