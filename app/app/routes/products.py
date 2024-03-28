from fastapi import APIRouter, HTTPException
from app.models.models import Product
from app.schemas.schemas import ProductSchema
from app.database.database import database
from typing import List
import uuid

router = APIRouter()

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
                category TEXT,
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
                active BOOLEAN,
                title TEXT,
                slug TEXT,
                duration INTEGER,
                totalSteps INTEGER,
                updatedAt TEXT,
                featured BOOLEAN,
                progress JSON,
                steps JSON,
                summaries JSON
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
                "category": "contracts",
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
                "title": "Dummy Product 1 Title",
                "slug": "dummy-product-1-slug",
                "duration": 30,
                "totalSteps": 3,
                "updatedAt": "2024-03-12T12:00:00",
                "featured": True,
                "progress": [{"currentStep": "1", "completed": "50"}],
                "steps": [
                    {
                        "order": 0,
                        "title": "Step 1",
                        "subtitle": "Subtitle 1",
                        "content": "Content 1"
                    },
                    {
                        "order": 1,
                        "title": "Step 2",
                        "subtitle": "Subtitle 2",
                        "content": "Content 2"
                    },
                    {
                        "order": 2,
                        "title": "Step 3",
                        "subtitle": "Subtitle 3",
                        "content": "Content 3"
                    }
                ],
                "summaries": [
                    {"summary_a": [{"model": "Model A", "summary": "Summary A"}]},
                    {"summary_b": [{"model": "Model B", "summary": "Summary B"}]}
                ]
            },
            # Dummy Product 2
            {
                "id": str(uuid.uuid4()),
                "name": "Dummy Product 2",
                "handle": "dummy-product-2",
                "description": "Another dummy product.",
                "category": "leases",
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
                "title": "Dummy Product 2 Title",
                "slug": "dummy-product-2-slug",
                "duration": 45,
                "totalSteps": 3,
                "updatedAt": "2024-03-12T13:30:00",
                "featured": False,
                "progress": [{"currentStep": "1", "completed": "60"}],
                "steps": [
                    {
                        "order": 0,
                        "title": "Step 1",
                        "subtitle": "Subtitle 1",
                        "content": "Content 1"
                    },
                    {
                        "order": 1,
                        "title": "Step 2",
                        "subtitle": "Subtitle 2",
                        "content": "Content 2"
                    },
                    {
                        "order": 2,
                        "title": "Step 3",
                        "subtitle": "Subtitle 3",
                        "content": "Content 3"
                    }
                ],
                "summaries": [
                    {"summary_a": [{"model": "Model A", "summary": "Lorem ipsum 1"}]},
                    {"summary_b": [{"model": "Model B", "summary": "Loreal ipsum 2"}]}
                ]
            },
            # Dummy Product 3
            {
                "id": str(uuid.uuid4()),
                "name": "Dummy Product 3",
                "handle": "dummy-product-3",
                "description": "Yet another dummy product.",
                "category": "contracts",
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
                "title": "Dummy Product 3 Title",
                "slug": "dummy-product-3-slug",
                "duration": 60,
                "totalSteps": 3,
                "updatedAt": "2024-03-12T15:00:00",
                "featured": True,
                "progress": [{"currentStep": "1", "completed": "100"}],
                "steps": [
                    {
                        "order": 0,
                        "title": "Step 1",
                        "subtitle": "Subtitle 1",
                        "content": "Content 1"
                    },
                    {
                        "order": 1,
                        "title": "Step 2",
                        "subtitle": "Subtitle 2",
                        "content": "Content 2"
                    },
                    {
                        "order": 2,
                        "title": "Step 3",
                        "subtitle": "Subtitle 3",
                        "content": "Content 3"
                    }
                ],
                "summaries": [
                    {"summary_a": [{"model": "Model A", "summary": "Okay dude"}]},
                    {"summary_b": [{"model": "Model B", "summary": "7 years and 4 cores"}]}
                ]
            }
        ]

        # Insert dummy records into the products table
        for product in products:
            await database.execute(Product.__table__.insert().values(product))

@router.post("/e-commerce/products", response_model=ProductSchema)
async def create_product(product: ProductSchema):
    new_product = product.dict()
    
    new_product["id"] = str(uuid.uuid4())
    
    # Assume description is the text you want to summarize
    description = new_product.get("description", "")
    
    if random.choice([True, False]):
        model_a = "gpt-4"
        model_b = "gpt-3.5-turbo-0613"
    else:
        model_a = "gpt-3.5-turbo-0613"
        model_b = "gpt-4"

    # Run summarize() on two different models
    summary_a_text = await summarize(model_a, description, prompt_template)
    summary_b_text = await summarize(model_b, description, prompt_template)

    # Here, you'll need to decide how to store these summaries.
    # For simplicity, let's add them directly to the product dict.
    # This approach depends entirely on how your database and models are set up.
    new_product["summaries"] = [
        {"summary_a": [{"model": model_a, "summary": summary_a_text}]},
        {"summary_b": [{"model": model_b, "summary": summary_b_text}]}
    ]

    query = Product.__table__.insert().values(new_product)
    product_id = await database.execute(query)

    # Fetch the created product by its ID and return it in the response
    created_product = await get_product_by_id(product_id)
    return created_product

# Helper function to get a product by ID
async def get_product_by_id(product_id: str):
    query = Product.__table__.select().where(Product.id == product_id)
    return await database.fetch_one(query)

import random

@router.put("/e-commerce/products/{product_id}", response_model=ProductSchema)
async def update_product(product_id: str, updated_product: ProductSchema):
    # Check if the product with the given ID exists
    existing_product = await get_product_by_id(product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Convert SQLAlchemy model instance to dictionary for easier manipulation
    existing_product_data = dict(existing_product)

    # Update the existing product data with new data from updated_product
    updated_product_data = updated_product.dict(exclude_unset=True)
    for key, value in updated_product_data.items():
        if key != "summaries":  # Exclude summaries from direct update
            existing_product_data[key] = value

    # Assume description is the text you want to summarize (from updated data if available)
    description = updated_product_data.get("description", existing_product_data.get("description", ""))

    if random.choice([True, False]):
        model_a = "gpt-4"
        model_b = "gpt-3.5-turbo-0613"
    else:
        model_a = "gpt-3.5-turbo-0613"
        model_b = "gpt-4"

    # Run summarize() on two different models
    summary_a_text = await summarize(model_a, description, prompt_template)
    summary_b_text = await summarize(model_b, description, prompt_template)

    # Update the summaries in existing_product_data
    existing_product_data["summaries"] = [
        {"summary_a": [{"model": model_a, "summary": summary_a_text}]},
        {"summary_b": [{"model": model_b, "summary": summary_b_text}]}
    ]

    # Commit the changes to the database
    query = Product.__table__.update().where(Product.id == product_id).values(existing_product_data)
    await database.execute(query)

    # Fetch the updated product by its ID and return it in the response
    updated_product = await get_product_by_id(product_id)
    return updated_product

# Function to get all records from the "products" table
async def get_all_products():
    query = Product.__table__.select()
    return await database.fetch_all(query)

#  New route to get all records from the "products" table
@router.get("/e-commerce/products", response_model=List[ProductSchema])
async def read_products():
    return await get_all_products()

@router.get("/e-commerce/products/{product_id}", response_model=ProductSchema)
async def read_product_by_id(product_id: str):
    query = Product.__table__.select().where(Product.id == product_id)
    product = await database.fetch_one(query)

    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")

# Route to create the database and insert dummy records
@router.post("/create_database")
async def create_database():
    try:
        await create_dummy_records()
        return {"message": "Database created successfully with dummy records."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@router.delete("/e-commerce/products/{product_id}", response_model=dict)
async def delete_product_by_id(product_id: str):
    query = Product.__table__.delete().where(Product.id == product_id)
    deleted_rows = await database.execute(query)

    if deleted_rows:
        return {"message": f"Product with ID {product_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

@router.delete("/e-commerce/products", response_model=dict)
async def delete_products(product_ids: List[str]):
    query = Product.__table__.delete().where(Product.id.in_(product_ids))
    deleted_rows = await database.execute(query)

    if deleted_rows:
        return {"message": f"{deleted_rows} product(s) deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="No matching products found for deletion")