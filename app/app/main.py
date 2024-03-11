from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, String, Float, Boolean, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from typing import List
from pydantic import BaseModel

# Define the SQLAlchemy model
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

# Define the FastAPI app
app = FastAPI()

# Configure the database URL
DATABASE_URL = "sqlite:///./test.db"

# Create the database engine and connect to it
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Create the database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the FastAPI database instance
database = Database(DATABASE_URL)

# Function to create the database and insert dummy records
async def create_dummy_records():
    async with database.transaction():
        # Create the tables
        await database.execute("DROP TABLE IF EXISTS products")
        await database.execute(
            """
            CREATE TABLE products (
                id TEXT PRIMARY KEY,
                name TEXT,
                handle TEXT,
                description TEXT,
                categories JSON,
                tags JSON,
                featuredImageId TEXT,
                images JSON,
                priceTaxExcl REAL,
                priceTaxIncl REAL,
                taxRate REAL,
                comparedPrice REAL,
                quantity REAL,
                sku TEXT,
                width TEXT,
                height TEXT,
                depth TEXT,
                weight TEXT,
                extraShippingFee REAL,
                active BOOLEAN
            )
            """
        )

        # Insert dummy records
        products = [
            # Dummy Product 1
            {
                "id": "1",
                "name": "Dummy Product 1",
                "handle": "dummy-product-1",
                "description": "This is a dummy product.",
                "categories": ["Dummy Category"],
                "tags": ["Dummy Tag"],
                "featuredImageId": "1",
                "images": [{"id": "1", "url": "image1.jpg"}],
                "priceTaxExcl": 50.0,
                "priceTaxIncl": 55.0,
                "taxRate": 10.0,
                "comparedPrice": 60.0,
                "quantity": 100,
                "sku": "SKU123",
                "width": "10cm",
                "height": "15cm",
                "depth": "5cm",
                "weight": "0.5kg",
                "extraShippingFee": 5.0,
                "active": True,
            },
            # Dummy Product 2
            {
                "id": "2",
                "name": "Dummy Product 2",
                "handle": "dummy-product-2",
                "description": "Another dummy product.",
                "categories": ["Dummy Category"],
                "tags": ["Dummy Tag"],
                "featuredImageId": "2",
                "images": [{"id": "2", "url": "image2.jpg"}],
                "priceTaxExcl": 75.0,
                "priceTaxIncl": 82.5,
                "taxRate": 10.0,
                "comparedPrice": 90.0,
                "quantity": 50,
                "sku": "SKU456",
                "width": "12cm",
                "height": "18cm",
                "depth": "6cm",
                "weight": "0.7kg",
                "extraShippingFee": 7.5,
                "active": True,
            },
            # Dummy Product 3
            {
                "id": "3",
                "name": "Dummy Product 3",
                "handle": "dummy-product-3",
                "description": "Yet another dummy product.",
                "categories": ["Dummy Category"],
                "tags": ["Dummy Tag"],
                "featuredImageId": "3",
                "images": [{"id": "3", "url": "image3.jpg"}],
                "priceTaxExcl": 100.0,
                "priceTaxIncl": 110.0,
                "taxRate": 10.0,
                "comparedPrice": 120.0,
                "quantity": 75,
                "sku": "SKU789",
                "width": "15cm",
                "height": "22cm",
                "depth": "8cm",
                "weight": "1.0kg",
                "extraShippingFee": 10.0,
                "active": True,
            },
        ]

        # Insert dummy records into the products table
        for product in products:
            await database.execute(Product.__table__.insert().values(product))

# Function to get all records from the "products" table
async def get_all_products():
    query = Product.__table__.select()
    return await database.fetch_all(query)

# Route to create the database and insert dummy records
@app.post("/create_database")
async def create_database():
    try:
        await create_dummy_records()
        return {"message": "Database created successfully with dummy records."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New route to get all records from the "products" table
@app.get("/products", response_model=List[ProductSchema])
async def read_products():
    return await get_all_products()
