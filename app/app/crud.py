# crud.py

from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from models import Product
import json

def create_table(db: Session):
    try:
        # Explicitly declare DROP TABLE statement
        drop_table_statement = text(
            """
            DROP TABLE IF EXISTS products
            """
        )

        # Create the tables
        db.execute(drop_table_statement)

        create_table_statement = text(
            """
            CREATE TABLE products (
                id TEXT PRIMARY KEY,
                name TEXT,
                handle TEXT,
                description TEXT,
                categories TEXT,  -- Change to TEXT for JSON
                tags TEXT,        -- Change to TEXT for JSON
                featuredImageId TEXT,
                images TEXT,      -- Change to TEXT for JSON
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

        db.execute(create_table_statement)
        print("Table created successfully.")

    except Exception as e:
        print(f"Error creating table: {e}")

def insert_dummy_records(db: Session):
    try:
        # Insert dummy records
        products = [
            # Dummy Product 1
            {
                "id": "1",
                "name": "Dummy Product 1",
                "handle": "dummy-product-1",
                "description": "This is a dummy product.",
                "categories": json.dumps(["Dummy Category"]),  # Convert to JSON-formatted string
                "tags": json.dumps(["Dummy Tag"]),  # Convert to JSON-formatted string
                "featuredImageId": "1",
                "images": json.dumps([{"id": "1", "url": "image1.jpg"}]),  # Convert to JSON-formatted string
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
                "categories": json.dumps(["Dummy Category"]),  # Convert to JSON-formatted string
                "tags": json.dumps(["Dummy Tag"]),  # Convert to JSON-formatted string
                "featuredImageId": "2",
                "images": json.dumps([{"id": "2", "url": "image2.jpg"}]),  # Convert to JSON-formatted string
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
                "categories": json.dumps(["Dummy Category"]),  # Convert to JSON-formatted string
                "tags": json.dumps(["Dummy Tag"]),  # Convert to JSON-formatted string
                "featuredImageId": "3",
                "images": json.dumps([{"id": "3", "url": "image3.jpg"}]),  # Convert to JSON-formatted string
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
            insert_statement = Product.__table__.insert().values(**product)
            print(f"Insert Statement: {insert_statement}")  # Print the SQL statement
            db.execute(insert_statement)
        print("Dummy records inserted successfully.")

    except Exception as e:
        print(f"Error inserting dummy records: {e}")

def get_all_products(db: Session):
    query = text("SELECT * FROM products")
    result = db.execute(query)
    return [dict(row) for row in result]
