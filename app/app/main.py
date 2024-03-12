from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Float, Boolean, JSON, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from typing import List
from pydantic import BaseModel
import uuid

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

class Sumdoc(Base):
    __tablename__ = "sumdocs"
    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    slug = Column(String)
    description = Column(String)
    category = Column(String)
    duration = Column(Integer)
    totalSteps = Column(Integer)
    updatedAt = Column(String)
    featured = Column(Boolean)
    progress = Column(JSON)


class SumdocSchema(BaseModel):
    id: str
    title: str
    slug: str
    description: str
    category: str
    duration: int
    totalSteps: int
    updatedAt: str
    featured: bool
    progress: List[dict]

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

# Configure CORS

origins = [
    "*",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

async def create_dummy_sumdocs():
    async with database.transaction():
        await database.execute("DROP TABLE IF EXISTS sumdocs")
        await database.execute(
            """
            CREATE TABLE sumdocs (
                id TEXT PRIMARY KEY,
                title TEXT,
                slug TEXT,
                description TEXT,
                category TEXT,
                duration INTEGER,
                totalSteps INTEGER,
                updatedAt TEXT,
                featured BOOLEAN,
                progress JSON
            )
            """
        )

        # Insert dummy records
        sumdocs = [
            {
                "id": str(uuid.uuid4()),
                "title": "Dummy Sumdoc 1",
                "slug": "dummy-sumdoc-1",
                "description": "This is a dummy sumdoc.",
                "category": "Dummy Category",
                "duration": 30,
                "totalSteps": 10,
                "updatedAt": "2024-03-12T12:00:00",
                "featured": True,
                "progress": [{"currentStep": "5", "completed": "50"}]
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Dummy Sumdoc 2",
                "slug": "dummy-sumdoc-2",
                "description": "Another dummy sumdoc.",
                "category": "Dummy Category",
                "duration": 45,
                "totalSteps": 15,
                "updatedAt": "2024-03-12T13:30:00",
                "featured": False,
                "progress": [{"currentStep": "8", "completed": "60"}]
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Dummy Sumdoc 3",
                "slug": "dummy-sumdoc-3",
                "description": "Yet another dummy sumdoc.",
                "category": "Dummy Category",
                "duration": 60,
                "totalSteps": 20,
                "updatedAt": "2024-03-12T15:00:00",
                "featured": True,
                "progress": [{"currentStep": "10", "completed": "100"}]
            },
        ]

        # Insert dummy records into the products table
        for sumdoc in sumdocs:
            await database.execute(Sumdoc.__table__.insert().values(sumdoc))

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
                "id": str(uuid.uuid4()),
                "name": "Dummy Product 1",
                "handle": "dummy-product-1",
                "description": "This is a dummy product.",
                "categories": ["Dummy Category"],
                "tags": ["Dummy Tag"],
                "featuredImageId": "1",
                "images": [{"id": "1", "url": "assets/images/apps/ecommerce/a-walk-amongst-friends.jpg"}],
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
                "id": str(uuid.uuid4()),
                "name": "Dummy Product 2",
                "handle": "dummy-product-2",
                "description": "Another dummy product.",
                "categories": ["Dummy Category"],
                "tags": ["Dummy Tag"],
                "featuredImageId": "2",
                "images": [{"id": "2", "url": "assets/images/apps/ecommerce/braies-lake.jpg"}],
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
                "id": str(uuid.uuid4()),
                "name": "Dummy Product 3",
                "handle": "dummy-product-3",
                "description": "Yet another dummy product.",
                "categories": ["Dummy Category"],
                "tags": ["Dummy Tag"],
                "featuredImageId": "3",
                "images": [{"id": "3", "url": "assets/images/apps/ecommerce/fall-glow.jpg"}],
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
@app.get("/e-commerce/products", response_model=List[ProductSchema])
async def read_products():
    return await get_all_products()

@app.get("/e-commerce/products/{product_id}", response_model=ProductSchema)
async def read_product_by_id(product_id: str):
    query = Product.__table__.select().where(Product.id == product_id)
    product = await database.fetch_one(query)

    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")
    

@app.delete("/e-commerce/products/{product_id}", response_model=dict)
async def delete_product_by_id(product_id: str):
    query = Product.__table__.delete().where(Product.id == product_id)
    deleted_rows = await database.execute(query)

    if deleted_rows:
        return {"message": f"Product with ID {product_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

@app.delete("/e-commerce/products", response_model=dict)
async def delete_products(product_ids: List[str]):
    query = Product.__table__.delete().where(Product.id.in_(product_ids))
    deleted_rows = await database.execute(query)

    if deleted_rows:
        return {"message": f"{deleted_rows} product(s) deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="No matching products found for deletion")
    

@app.post("/e-commerce/products", response_model=ProductSchema)
async def create_product(product: ProductSchema):
    new_product = product.dict()
    new_product["id"] = str(uuid.uuid4())
    print(new_product["id"])
    query = Product.__table__.insert().values(new_product)
    product_id = await database.execute(query)

    # Fetch the created product by its ID and return it in the response
    created_product = await get_product_by_id(product_id)
    return created_product

# Helper function to get a product by ID
async def get_product_by_id(product_id: str):
    query = Product.__table__.select().where(Product.id == product_id)
    return await database.fetch_one(query)


@app.put("/e-commerce/products/{product_id}", response_model=ProductSchema)
async def update_product(product_id: str, updated_product: ProductSchema):
    # Check if the product with the given ID exists
    existing_product = await get_product_by_id(product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update the existing product with the new data
    updated_product_data = updated_product.dict(exclude_unset=True)
    for key, value in updated_product_data.items():
        setattr(existing_product, key, value)

    # Commit the changes to the database
    query = Product.__table__.update().where(Product.id == product_id).values(updated_product_data)
    await database.execute(query)

    # Return the updated product
    return existing_product

# Route to create the database and insert dummy records
@app.post("/initialize_sumdocs")
async def create_database():
    try:
        await create_dummy_sumdocs()
        return {"message": "Database created successfully with dummy records."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to get all records from the "products" table
async def get_all_sumdocs():
    query = Sumdoc.__table__.select()
    return await database.fetch_all(query)

# New route to get all records from the "products" table
@app.get("/summarizer/sumdocs", response_model=List[SumdocSchema])
async def read_sumdocs():
    return await get_all_sumdocs()