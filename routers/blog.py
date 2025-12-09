import os
import uuid

from fastapi import APIRouter, Request, Depends, Form, File, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from db import SessionLocal
from models.blog import BlogPost
from models.blog_media import BlogMedia

router = APIRouter(prefix="/admin", tags=["Admin (blog)"])
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "static/uploads/blog"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/blog", summary='список постов в админке')
def admin_blog(request: Request, db: Session = Depends(get_db)):
    posts = db.query(BlogPost).order_by(BlogPost.date_create.desc()).all()
    return templates.TemplateResponse("admin/admin_blog.html", {"request": request, "posts": posts})


@router.get("/blog/create", summary='форма создания')
def blog_create_form(request: Request):
    return templates.TemplateResponse("admin/blog_create.html", {"request": request})


@router.post("/blog/create", summary='создание поста (с загрузкой нескольких изображений)')
async def blog_create(
    title: str = Form(...),
    slug: str = Form(None),
    excerpt: str = Form(""),
    content: str = Form(""),
    images: list[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    post = BlogPost(title=title, slug=slug, excerpt=excerpt, content=content)
    db.add(post)
    db.commit()
    db.refresh(post)

    if images:
        for up in images:
            if not up.filename:
                continue
            ext = up.filename.split(".")[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            path = os.path.join(UPLOAD_DIR, filename)
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            with open(path, "wb") as f:
                f.write(await up.read())
            media = BlogMedia(filename=filename, post_id=post.id)
            db.add(media)
        db.commit()

    return RedirectResponse("/admin/blog", status_code=303)


@router.get("/blog/edit/{post_id}", summary='форма редактирования')
def blog_edit_form(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter_by(id=post_id).first()
    if not post:
        return RedirectResponse("/admin/blog", status_code=302)
    return templates.TemplateResponse("admin/blog_edit.html", {"request": request, "post": post})


@router.post("/blog/edit/{post_id}", summary='редактирование')
async def blog_edit(
    post_id: int,
    title: str = Form(...),
    slug: str = Form(None),
    excerpt: str = Form(""),
    content: str = Form(""),
    images: list[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    post = db.query(BlogPost).filter_by(id=post_id).first()
    if not post:
        return RedirectResponse("/admin/blog", status_code=302)

    post.title = title
    post.slug = slug
    post.excerpt = excerpt
    post.content = content
    db.commit()

    if images:
        for up in images:
            if not up.filename:
                continue
            ext = up.filename.split(".")[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            path = os.path.join(UPLOAD_DIR, filename)
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            with open(path, "wb") as f:
                f.write(await up.read())
            media = BlogMedia(filename=filename, post_id=post.id)
            db.add(media)
        db.commit()

    return RedirectResponse(f"/admin/blog/edit/{post_id}", status_code=303)


@router.post("/blog/{post_id}/media/{media_id}/delete", summary='удалить медиа')
def blog_delete_media(post_id: int, media_id: int, db: Session = Depends(get_db)):
    media = db.query(BlogMedia).filter_by(id=media_id, post_id=post_id).first()
    if media:
        filepath = os.path.join(UPLOAD_DIR, media.filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass
        db.delete(media)
        db.commit()
    return RedirectResponse(f"/admin/blog/edit/{post_id}", status_code=303)


@router.post("/blog/{post_id}/delete", summary='удалить пост полностью')
def blog_delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter_by(id=post_id).first()
    if not post:
        return RedirectResponse("/admin/blog", status_code=302)
    for m in post.media:
        path = os.path.join(UPLOAD_DIR, m.filename)
        if os.path.exists(path):
            try:
                os.remove(path)
            except:
                pass
    db.delete(post)
    db.commit()
    return RedirectResponse("/admin/blog", status_code=303)
