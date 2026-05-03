import asyncio

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

from rag.loader import load_pdf
from rag.chunker import split_documents
from rag.vectorstore import create_vectorstore, get_retriever
from rag.chain import build_chain

# Streamlit Cloud: read from secrets if available
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

st.set_page_config(page_title="PDF Chat", page_icon="📄")
st.title("📄 Chat with your PDF")
st.caption("Powered by Gemini 2.5 Flash + LangChain RAG — Free tier")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chain" not in st.session_state:
    st.session_state.chain = None

with st.sidebar:
    st.header("📂 Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file:
        if st.button("🚀 Process PDF"):
            with st.spinner("Reading and indexing your PDF..."):
                docs = load_pdf(uploaded_file)
                chunks = split_documents(docs)
                vectorstore = create_vectorstore(chunks)
                retriever = get_retriever(vectorstore)
                st.session_state.chain = build_chain(retriever)
                st.session_state.messages = []
            st.success(f"✅ Done! {len(chunks)} chunks indexed.")
    if st.session_state.chain:
        st.info("PDF is ready. Ask anything below!")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if query := st.chat_input("Ask a question about your PDF..."):
    if not st.session_state.chain:
        st.warning("⚠️ Please upload and process a PDF first.")
    else:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.write(query)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = st.session_state.chain({"query": query})
                answer = result["result"]
                sources = result.get("source_documents", [])
                st.write(answer)
                if sources:
                    with st.expander("📎 Source pages"):
                        for doc in sources:
                            page = doc.metadata.get("page", "?")
                            st.caption(f"Page {page+1}: {doc.page_content[:200]}...")
        st.session_state.messages.append({"role": "assistant", "content": answer})