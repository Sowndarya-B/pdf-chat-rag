from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import TOP_K

def create_vectorstore(chunks):

    # Optional: limit for testing
    chunks = chunks[:50]

    # ✅ Use LOCAL embeddings (no API)
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore


def get_retriever(vectorstore):
    return vectorstore.as_retriever(search_kwargs={"k": TOP_K})