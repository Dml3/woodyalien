from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from schemas.blog import BlogCreate, BlogOut
import json

router = APIRouter(prefix="/api/blog", tags=["Blog"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()