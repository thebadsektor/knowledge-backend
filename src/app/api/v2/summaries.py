import uuid
import random
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI

from models.models import Sumdoc
from schemas.schemas import SumdocSchema
from database.database import database
from fastapi.encoders import jsonable_encoder

from worker import summarize_task

router = APIRouter()


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


@router.post("/documents", response_model=SumdocSchema, tags=["Summaries v2"])
async def create_document(sumdoc: SumdocSchema):
    new_sumdoc = sumdoc.dict()
    
    new_sumdoc["id"] = str(uuid.uuid4())
    
    # Assume description is the text you want to summarize
    description = new_sumdoc.get("description", "")
    
    if random.choice([True, False]):
        model_a = "gpt-4"
        model_b = "gpt-3.5-turbo-0613"
    else:
        model_a = "gpt-3.5-turbo-0613"
        model_b = "gpt-4"

    # Run summarize() on two different models
    summary_a_task = await summarize(model_a, description, prompt_template)
    summary_b_task = await summarize(model_b, description, prompt_template)

    # Here, you'll need to decide how to store these summaries.
    # For simplicity, let's add them directly to the sumdoc dict.
    # This approach depends entirely on how your database and models are set up.
    new_sumdoc["summaries"] = [
        {"summary_a": [{"model": model_a, "summary": summary_a_task}]},
        {"summary_b": [{"model": model_b, "summary": summary_b_task}]}
    ]

    query = Sumdoc.__table__.insert().values(new_sumdoc)
    document_id = await database.execute(query)

    # Fetch the created Sumdoc by its ID and return it in the response
    created_sumdoc = await get_document_by_id(document_id)
    return created_sumdoc

# Helper function to get a Sumdoc by ID
async def get_document_by_id(document_id: str):
    query = Sumdoc.__table__.select().where(Sumdoc.id == document_id)
    return await database.fetch_one(query)

@router.put("/documents/{document_id}", response_model=SumdocSchema, tags=["Summaries v2"])
async def update_document(document_id: str, updated_sumdoc: SumdocSchema):
    # Check if the Sumdoc with the given ID exists

    existing_sumdoc = await get_document_by_id(document_id)
    if not existing_sumdoc:
        raise HTTPException(status_code=404, detail="Sumdoc not found")

    # Convert SQLAlchemy model instance to dictionary for easier manipulation
    existing_sumdoc_data = dict(existing_sumdoc)

    # Update the existing Sumdoc data with new data from updated_sumdoc
    updated_sumdoc_data = updated_sumdoc.dict(exclude_unset=True)
    for key, value in updated_sumdoc_data.items():
        if key != "summaries":  # Exclude summaries from direct update
            existing_sumdoc_data[key] = value

    # Assume description is the text you want to summarize (from updated data if available)
    description = updated_sumdoc_data.get("description", existing_sumdoc_data.get("description", ""))

    if random.choice([True, False]):
        model_a = "gpt-4"
        model_b = "gpt-3.5-turbo-0613"
    else:
        model_a = "gpt-3.5-turbo-0613"
        model_b = "gpt-4"

    # Run summarize() on two different models
    summary_a_text = await summarize(model_a, description, prompt_template)
    summary_b_text = await summarize(model_b, description, prompt_template)

    # Update the summaries in existing_sumdoc_data
    existing_sumdoc_data["summaries"] = [
        {"summary_a": [{"model": model_a, "summary": summary_a_text}]},
        {"summary_b": [{"model": model_b, "summary": summary_b_text}]}
    ]

    # Commit the changes to the database
    query = Sumdoc.__table__.update().where(Sumdoc.id == document_id).values(existing_sumdoc_data)
    await database.execute(query)

    # Fetch the updated Sumdoc by its ID and return it in the response
    updated_sumdoc = await get_document_by_id(document_id)
    return updated_sumdoc
    

@router.post("/summarize-task", status_code=201, tags=["Summarization Tasks v2"],
          description="""
          Submit a single document for summarization from a text file:
          
          - document-1-357-1697.txt (357 Tokens): Will and Estate
          
          The operation returns task IDs for the summarization task.
          """)
def summarize_task_endpoint():
    model = "gpt-3.5-turbo-0613"
    document_1 = read_text_file("documents/document-1-357-1697.txt")
    task_1 = summarize_task.delay(model, document_1)
    return JSONResponse({"task_ids": {"document_1": task_1.id}})


@router.post("/batch-summarize-task", status_code=201, tags=["Summarization Tasks v2"],
          description="""
          Submit multiple documents for summarization. Each document content should be passed as a plain text input.
          
          This endpoint is designed to submit 10 summarization tasks from text files:
          
          - document-1-357-1697.txt (357 Tokens): Will and Estate
          - document-2-2035-10856.txt (2,035 Tokens): Environmental Policy
          - document-3-388-1786.txt (388 Tokens): Will and Estate
          - document-4-733-3229.txt (733 Tokens): Will and Estate
          - document-5-649-2820.txt (649 Tokens): Will and Estate
          - document-6-1401-7828.txt (1,201 Tokens): Marketing Services Agreement
          - document-7-1008-5201.txt (1,008 Tokens): Website Development Agreement
          - document-8-1047-5303.txt (1,047 Tokens): Website Development Agreement
          - document-9-825-4318.txt (825 Tokens): Non-Disclosure Agrement
          - document-10-1173-5362.txt (1,173 Tokens): Loan Agreement
          
          Returns a dictionary of task IDs for each summarization task.
          """)
def batch_summarize_task_endpoint():
    
    model = "gpt-3.5-turbo-0613"
    document_1 = read_text_file("documents/document-1-357-1697.txt")
    document_2 = read_text_file("documents/document-2-2035-10856.txt")
    document_3 = read_text_file("documents/document-3-388-1786.txt")
    document_4 = read_text_file("documents/document-4-733-3229.txt")
    document_5 = read_text_file("documents/document-5-649-2820.txt")
    document_6 = read_text_file("documents/document-6-1401-7828.txt")
    document_7 = read_text_file("documents/document-7-1008-5201.txt")
    document_8 = read_text_file("documents/document-8-1047-5303.txt")
    document_9 = read_text_file("documents/document-9-825-4318.txt")
    document_10 = read_text_file("documents/document-10-1173-5362.txt")
    task_1 = summarize_task.delay(model, document_1)
    task_2 = summarize_task.delay(model, document_2)
    task_3 = summarize_task.delay(model, document_3)
    task_4 = summarize_task.delay(model, document_4)
    task_5 = summarize_task.delay(model, document_5)
    task_6 = summarize_task.delay(model, document_6)
    task_7 = summarize_task.delay(model, document_7)
    task_8 = summarize_task.delay(model, document_8)
    task_9 = summarize_task.delay(model, document_9)
    task_10 = summarize_task.delay(model, document_10)
    return JSONResponse({
        "task_ids": {
            "document_1": task_1.id,
            "document_2": task_2.id,
            "document_3": task_3.id,
            "document_4": task_4.id,
            "document_5": task_5.id,
            "document_6": task_6.id,
            "document_7": task_7.id,
            "document_8": task_8.id,
            "document_9": task_9.id,
            "document_10": task_10.id
        }
    })


def read_text_file(file_path: str) -> str:
    """Utility function to read text from a given file path."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
