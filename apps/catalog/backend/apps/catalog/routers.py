# Made by Kaléin Tamaríz
import os
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db import get_db
from .models import Product, Category
from .schemas import CategorySchema, ProductResponse

router = APIRouter(prefix="/api")

BASE_MEDIA_URL = os.getenv("BASE_MEDIA_URL", "/media")

@router.get("/categories", response_model=list[CategorySchema])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/products", response_model=list[ProductResponse])
def get_products(category_id: int = Query(None), db: Session = Depends(get_db)):
    query = db.query(Product)
    if category_id:
        query = query.join(Product.categories).filter(Category.id == category_id)
    
    products = query.all()
    results = []
    for p in products:
        # Build category names list
        cat_names = [c.name for c in p.categories]
        
        # Build media list with absolute URLs
        media_list = []
        primary_image = None
        for m in p.media:
            m_url = m.media_url
            if not m_url.startswith("http"):
                m_url = f"{BASE_MEDIA_URL}/{m_url}"
            
            media_list.append({
                "media_url": m_url,
                "is_primary": m.is_primary,
                "position": m.position
            })
            if m.is_primary:
                primary_image = m_url
        
        results.append(ProductResponse(
            id=p.id,
            name=p.name,
            price=p.price,
            description=p.description,
            categories=cat_names,
            media=media_list,
            primary_image=primary_image
        ))
    return results
