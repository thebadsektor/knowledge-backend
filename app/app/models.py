from sqlalchemy import Column, String, Float, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    handle = Column(String)
    description = Column(String)
    categories = Column(JSON)
    tags = Column(JSON)
    featuredImageId = Column(String)
    images = Column(JSON)
    priceTaxExcl = Column(Float)
    priceTaxIncl = Column(Float)
    taxRate = Column(Float)
    comparedPrice = Column(Float)
    quantity = Column(Float)
    sku = Column(String)
    width = Column(String)
    height = Column(String)
    depth = Column(String)
    weight = Column(String)
    extraShippingFee = Column(Float)
    active = Column(Boolean)

class ProductSchema(BaseModel):
    id: str
    name: str
    handle: str
    description: str
    categories: List[str]
    tags: List[str]
    featuredImageId: str
    images: List[dict]
    priceTaxExcl: float
    priceTaxIncl: float
    taxRate: float
    comparedPrice: float
    quantity: float
    sku: str
    width: str
    height: str
    depth: str
    weight: str
    extraShippingFee: float
    active: bool