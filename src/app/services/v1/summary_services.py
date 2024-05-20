from openai import OpenAI
import uuid

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

document = """
    Test document.
"""

model = "gpt-3.5-turbo-0613"
    

async def summarize(api_key, model=model, document=document, prompt_template=prompt_template, max_length=4000):

    # Format the prompt with truncated text
    prompt = prompt_template.format(document=document)
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        # model="text-davinci-003",  # Lighter model
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        # max_tokens=512
    ).choices[0].message.content.strip()

    return response

async def create_summarization(api_key, model=model, document=document, prompt_template=prompt_template, doc_id=None, max_length=4000):

    # Format the prompt with truncated text
    prompt = prompt_template.format(document=document)
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        # model="text-davinci-003",  # Lighter model
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        # max_tokens=512
    ).choices[0].message.content.strip()
    
    return response