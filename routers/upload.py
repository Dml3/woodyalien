from fastapi import APIRouter, UploadFile, File
import os
import uuid

router = APIRouter(prefix="/upload")

UPLOAD_FOLDER = "static/uploads/products"


@router.post("/product")
async def upload_product_image(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # создаём папку если нет
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # сохраняем файл
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    return {"filename": filename}
