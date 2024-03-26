# TODO: Disconnect from Products
from fastapi import APIRouter, HTTPException
from app.models.models import Product
from app.models.models import Sumdoc
from app.schemas.schemas import ProductSchema
from app.schemas.schemas import SumdocSchema
from app.database.database import database
from typing import List
import uuid

router = APIRouter()

async def create_dummy_sumdocs():
    async with database.transaction():
        await database.execute("DROP TABLE IF EXISTS sumdocs")
        await database.execute(
            """
            CREATE TABLE sumdocs (
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
        sumdocs = [
            {
                "id": str(uuid.uuid4()),
                "name": "Dummy Product 1",
                "handle": "dummy-document-1",
                "description": "This is a dummy document.",
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
                "title": "Dummy Document 1 Title",
                "slug": "dummy-document-1-slug",
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
                "handle": "dummy-document-2",
                "description": "Another dummy document.",
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
                "title": "Dummy Document 2 Title",
                "slug": "dummy-document-2-slug",
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
            # Dummy Product 4
            {
                "id": str(uuid.uuid4()),
                "name": "Eco-Friendly Water Bottle",
                "handle": "eco-friendly-water-bottle",
                "description": "A sustainable, durable water bottle for everyday use.",
                "category": "Eco Products",
                "categories": ["Sustainable Goods"],
                "tags": ["Eco-Friendly", "Water Bottle", "Sustainable"],
                "featuredImageId": "101",
                "images": [
                    {
                    "id": "101",
                    "url": "assets/images/products/eco-friendly-water-bottle.jpg"
                    }
                ],
                "priceTaxExcl": 25.0,
                "priceTaxIncl": 27.5,
                "taxRate": 10.0,
                "comparedPrice": 30.0,
                "quantity": 150,
                "sku": "EFWB1001",
                "width": "7cm",
                "height": "25cm",
                "depth": "7cm",
                "weight": "0.3kg",
                "extraShippingFee": 5.0,
                "active": True,
                "title": "Stay Hydrated, Stay Green",
                "slug": "eco-friendly-water-bottle",
                "duration": 120,
                "totalSteps": 2,
                "updatedAt": "2024-05-20T10:00:00",
                "featured": False,
                "progress": [{"currentStep": "1", "completed": "50"}],
                "steps": [
                    {
                    "order": 0,
                    "title": "Introduction to Sustainability",
                    "subtitle": "Understanding the Impact",
                    "content": "Exploring the importance of sustainability in everyday products."
                    },
                    {
                    "order": 1,
                    "title": "Product Usage and Care",
                    "subtitle": "Maximizing Lifespan",
                    "content": "Tips on using and caring for your water bottle to ensure it lasts a lifetime."
                    }
                ],
                "summaries": [
                    {
                    "summary_a": [{"model": "Model Green", "summary": "Every sip supports sustainability."}]
                    },
                    {
                    "summary_b": [{"model": "Model Blue", "summary": "Designed for durability and eco-friendliness."}]
                    }
                ]
            }
        ]

        # Insert dummy records into the products table
        for sumdoc in sumdocs:
            await database.execute(Sumdoc.__table__.insert().values(sumdoc))


# async def summarize(model: str, text: str) -> List[Dict[str, Any]]:
#     # Simulate an asynchronous call to generate summaries
#     await asyncio.sleep(1)  # Simulating async I/O operation
#     return f"Summrized {text[:50]} using {model}."

prompt_template = """
    You are an attorney who has been given part of a document enclosed below in <document> tags.

    This is part of a document that is a  will or trust document, outlining the distribution of life insurance proceeds to the author's children, john and sally washington. it specifies different distribution methods depending on whether the children are over or under the age of 21 at the time of the author's death.
    <document>
    {document}
    </document>

    Follow these instructions:
    1. Generate a highly detailed summary of all the important information in <document>. Be sure to emphasize and include details that could be of importance to a lawyer.
    2. Do not omit any important details or facts, include all important details such as names of persons, their title or relation to the matter, and any important dates or events mentioned in the document. Avoid vague statements, opting to provide a deep examination of the material in <document>.
    3. If parts of <document> are sub-divided into sections (and possible subsections), utilize prefixing and indentation to conform the format of the summary to a hierarchical outline.
    4. If referencing acronyms within your response, display the full title associated with the acronym once, then use the acronym for further repetitions.
    5. For each item within your summary, determine if there is any is missing information in your summary. Include all potential missing information in addition to the information already in your summary.
        Missing information can include:
            dates, times, durations
            length of passages
            locations
            cases
            quote context,
            relevant exchanges between individuals
            parties of contracts
            agreements within contracts
            proper nouns (people, groups, locations)
            terminology and systems (ex: a method for ranking, a set of criteria)
            terms, conditions, requirements
    6. It is better to be over-inclusive rather than under-inclusive. If you are unsure if you should include something which may or may not be important, always err on the side of caution and include the information.


    Give your answer in the following format:

    - Key point discussion...
    - Key point discussion...
    - Key point discussion...
    ...

    """

async def summarize(model, document, prompt_template, max_length=4000):

    # Format the prompt with truncated text
    prompt = prompt_template.format(document=document)
    client = OpenAI()
    response = client.chat.completions.create(
        # model="text-davinci-003",  # Lighter model
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        # max_tokens=512
    ).choices[0].message.content.strip()

    return response


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

# Route to create the database and insert dummy records
@router.post("/initialize_sumdocs")
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
@router.get("/summarizer/sumdocs", response_model=List[SumdocSchema])
async def read_sumdocs():
    return await get_all_sumdocs()

@router.get("/summarizer/sumdocs/{sumdoc_id}", response_model=SumdocSchema)
async def read_sumdoc_id_by_id(sumdoc_id: str):
    query = Sumdoc.__table__.select().where(Sumdoc.id == sumdoc_id)
    sumdoc = await database.fetch_one(query)

    if sumdoc:
        return sumdoc
    else:
        raise HTTPException(status_code=404, detail="Document not found")
