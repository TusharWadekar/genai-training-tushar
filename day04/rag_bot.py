import os
import glob
from dotenv import load_dotenv
from google import genai
from google.genai import types
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Step 1: Set up the vector database
chroma_client = chromadb.Client()
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
collection = chroma_client.get_or_create_collection(
    name="acc_bank_faqs",
    embedding_function=embedding_fn
)

# Step 2: Load documents and add them to the vector database
doc_files = glob.glob("day04/docs/*.txt")
for i, filepath in enumerate(doc_files):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    collection.add(
        documents=[content],
        ids=[f"doc_{i}"],
        metadatas=[{"source": os.path.basename(filepath)}]
    )

print(f"Loaded {len(doc_files)} documents into the vector database.\n")


def answer_question(question: str) -> str:
    # Step 3: Retrieve the most relevant document(s)
    results = collection.query(
        query_texts=[question],
        n_results=2
    )
    retrieved_docs = results["documents"][0]
    retrieved_sources = [m["source"] for m in results["metadatas"][0]]

    context = "\n\n".join(retrieved_docs)

    # Step 4: Ask the AI to answer ONLY using the retrieved context
    system_prompt = f"""You are a customer support assistant for ACC Bank.
Answer the customer's question using ONLY the information in the context below.
If the answer is not in the context, say "I don't have that information, please 
contact our support team." Do not make up any information.

Context:
{context}
"""

    resp = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=question,
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )

    print(f"Q: {question}")
    print(f"A: {resp.text}")
    print(f"(Sources used: {retrieved_sources})")
    print("---")


if __name__ == "__main__":
    test_questions = [
        "How do I block my debit card if it's stolen?",
        "What is the FD interest rate for 3 years?",
        "What is the loan interest rate for home loans?",  # not in docs - should say "I don't know"
    ]
    for q in test_questions:
        answer_question(q)