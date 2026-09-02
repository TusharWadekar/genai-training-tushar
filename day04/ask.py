import os
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

SYSTEM_TEMPLATE = """You are a customer support assistant for ACC Bank.
Answer the customer's question using ONLY the information in the context below.
After every fact you state, cite the source filename in square brackets, e.g. [kyc_requirements.txt].
If the context does not contain the answer, reply with EXACTLY this sentence and nothing else:
"I don't have that information in my knowledge base — let me connect you to a human agent."

Context:
{context}
"""


def ask(question: str):
    docs = retriever.invoke(question)
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

    print(f"Q: {question}")
    print(f"Sources retrieved: {sources}")
    print(f"A: {resp.text}")
    print("---")


if __name__ == "__main__":
    questions = [
        # 3 answerable
        "How do I hotlist my debit card if it's stolen?",
        "What is the daily UPI transaction limit?",
        "What documents do I need for KYC?",
        # 2 deliberately unanswerable
        "What is today's USD-INR exchange rate?",
        "What are the charges for the Platinum Sapphire card?",
    ]
    for q in questions:
        ask(q)