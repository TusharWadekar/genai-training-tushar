import os
import time
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 3})

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def expand_query(question: str) -> list:
    """Ask the AI to rephrase the question 3 different ways."""
    prompt = f"""Generate 3 different ways to rephrase this customer question, 
each on its own line, no numbering, no extra text:

Question: {question}"""

    for attempt in range(3):
        try:
            resp = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            variations = [line.strip() for line in resp.text.strip().split("\n") if line.strip()]
            return variations[:3]
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                wait_time = 15 * (attempt + 1)
                print(f"Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                raise
    """Ask the AI to rephrase the question 3 different ways."""
    prompt = f"""Generate 3 different ways to rephrase this customer question, 
each on its own line, no numbering, no extra text:

Question: {question}"""

    resp = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    variations = [line.strip() for line in resp.text.strip().split("\n") if line.strip()]
    return variations[:3]


def multi_retrieve(question: str):
    """Retrieve chunks using the original question + 3 variations, deduplicated."""
    all_queries = [question] + expand_query(question)

    seen_content = set()
    unique_docs = []

    for q in all_queries:
        docs = retriever.invoke(q)
        for d in docs:
            if d.page_content not in seen_content:
                seen_content.add(d.page_content)
                unique_docs.append(d)

    return unique_docs, all_queries


SYSTEM_TEMPLATE = """You are a customer support assistant for ACC Bank.
Answer the customer's question using ONLY the information in the context below.
After every fact you state, cite the source filename in square brackets, e.g. [kyc_requirements.txt].
If the context does not contain the answer, reply with EXACTLY this sentence and nothing else:
"I don't have that information in my knowledge base — let me connect you to a human agent."

Context:
{context}
"""


def ask_multi(question: str):
    docs, all_queries = multi_retrieve(question)
    sources = [d.metadata.get("source", "unknown") for d in docs]
    context = "\n\n".join(
        f"[{d.metadata.get('source', 'unknown')}]\n{d.page_content}" for d in docs
    )

    system_prompt = SYSTEM_TEMPLATE.format(context=context)

    resp = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=question,
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )

    print(f"Original Q: {question}")
    print(f"Query variations used: {all_queries}")
    print(f"Unique sources retrieved: {sources}")
    print(f"A: {resp.text}")
    print("---")


if __name__ == "__main__":
    test_question = "I need to know my UPI daily limit and also what documents are required for KYC"
    ask_multi(test_question)