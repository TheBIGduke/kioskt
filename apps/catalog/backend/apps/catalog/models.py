# Made by Kaléin Tamaríz
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

# Junction table for many-to-many relationship between products and categories
product_categories = Table(
    'product_categories',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    products = relationship("Product", secondary=product_categories, back_populates="categories")

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    categories = relationship("Category", secondary=product_categories, back_populates="products")
    media = relationship("ProductMedia", back_populates="product")

class ProductMedia(Base):
    __tablename__ = 'product_media'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    media_url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)
    position = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="media")
