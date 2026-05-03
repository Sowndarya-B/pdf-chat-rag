# 🔐 pdf-rag-chat

> Chat with your PDFs using Retrieval-Augmented Generation (RAG) — answers grounded in your documents, not LLM memory. Fully free with Google Gemini + HuggingFace Embeddings.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.1+-green?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=flat-square&logo=streamlit)
![HuggingFace](https://img.shields.io/badge/Embeddings-HuggingFace-yellow?style=flat-square&logo=huggingface)
![Gemini](https://img.shields.io/badge/LLM-Gemini%202.5%20Flash-blue?style=flat-square&logo=google)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

---

## ✨ Overview

**pdf-rag-chat** transforms static PDF documents into interactive, queryable knowledge sources. Instead of relying on raw LLM memory or guesswork, every response is strictly grounded in the content of your uploaded document using a Retrieval-Augmented Generation (RAG) pipeline.

Embeddings are generated locally using **HuggingFace sentence-transformers** — no API key or cost required for the embedding step. The LLM layer uses **Google Gemini 2.5 Flash** on the free tier.

Upload a PDF → Ask questions → Get precise, source-backed answers. 100% free.

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌───────────────────────────┐
│  PDF Upload  │ ──▶ │  Text Chunking   │ ──▶ │  HuggingFace Embeddings   │
└─────────────┘     └──────────────────┘     │  (sentence-transformers)  │
                                              └────────────┬──────────────┘
                                                           │
                                                  ┌────────▼──────────┐
                                                  │   FAISS Vector    │
                                                  │      Store        │
                                                  └────────┬──────────┘
                                                           │
┌─────────────┐     ┌──────────────────┐         ┌────────▼──────────┐
│  User Query │ ──▶ │ Semantic Retrieval│ ──────▶ │  Gemini 2.5 Flash │
└─────────────┘     └──────────────────┘         └────────┬──────────┘
                                                           │
                                                  ┌────────▼──────────┐
                                                  │  Grounded Answer  │
                                                  └───────────────────┘
```

---

## 🚀 Features

- 📄 **PDF Ingestion** — Upload any PDF and convert it into a queryable knowledge base
- 🤗 **HuggingFace Embeddings** — Local sentence-transformers model, no API key needed for embeddings
- 🧠 **FAISS Vector Store** — Fast in-memory similarity search over document chunks
- 🔗 **LangChain Orchestration** — Clean chain architecture connecting retrieval, context injection, and generation
- ✨ **Gemini 2.5 Flash LLM** — Free Google Gemini tier for intelligent response generation
- 🎯 **Document-Grounded Answers** — LLM responses strictly constrained to document content
- 💬 **Conversational UI** — Streamlit-powered chat interface with session history
- 📎 **Source Page References** — Each answer shows which pages the context was pulled from
- 🔒 **No Hallucination Policy** — Prompt enforces "I don't know" when content isn't in the document

---

## 🛠️ Tech Stack

| Layer | Technology | Cost |
|---|---|---|
| Language | Python 3.10+ | Free |
| RAG Framework | LangChain | Free |
| Embeddings | HuggingFace sentence-transformers | Free (local) |
| Vector Store | FAISS (in-memory) | Free |
| LLM | Google Gemini 2.5 Flash | Free tier |
| PDF Parsing | PyPDF | Free |
| UI | Streamlit | Free |
| Hosting | Streamlit Cloud | Free |

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/pdf-rag-chat.git
cd pdf-rag-chat
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ The first run will automatically download the HuggingFace embedding model (`all-MiniLM-L6-v2`, ~90MB). This only happens once and is cached locally.

### 4. Get your free Gemini API key

1. Visit [aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **Get API Key** → **Create API key**
4. Copy the key (starts with `AIzaSy...`)

### 5. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
GOOGLE_API_KEY=AIzaSy_your_key_here
```

### 6. Run the app

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📂 Project Structure

```
pdf-rag-chat/
├── .streamlit/
│   └── secrets.toml          # Streamlit Cloud secrets (never commit)
├── rag/
│   ├── __init__.py
│   ├── loader.py             # PDF ingestion via PyPDFLoader
│   ├── chunker.py            # RecursiveCharacterTextSplitter
│   ├── vectorstore.py        # HuggingFace embeddings + FAISS index
│   ├── chain.py              # LangChain RetrievalQA chain
│   └── prompt.py             # Grounded answer prompt template
├── app.py                    # Streamlit entry point
├── config.py                 # App-wide constants
├── requirements.txt
├── .env                      # Local secrets (never commit)
├── .env.example              # Template committed to git
├── .gitignore
└── README.md
```

---

## 🤗 HuggingFace Embeddings

This project uses **`all-MiniLM-L6-v2`** from HuggingFace sentence-transformers as the embedding model.

```python
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)
```

**Why `all-MiniLM-L6-v2`?**

| Property | Value |
|---|---|
| Model size | ~90 MB |
| Embedding dimensions | 384 |
| Speed | Very fast on CPU |
| Quality | Excellent for semantic search |
| Cost | Completely free, runs locally |

No HuggingFace API key is required — the model runs entirely on your local machine.

---

## 🔍 How It Works

1. **Ingestion** — The uploaded PDF is parsed and split into overlapping text chunks using LangChain's `RecursiveCharacterTextSplitter` (chunk size: 1000, overlap: 200).
2. **Embedding** — Each chunk is converted to a 384-dimensional vector using the local HuggingFace `all-MiniLM-L6-v2` model and stored in a FAISS index.
3. **Retrieval** — On each query, the top-k most semantically similar chunks are retrieved via cosine similarity search.
4. **Generation** — Retrieved chunks are injected into a LangChain prompt as context. Gemini 2.5 Flash generates an answer grounded exclusively in that context.
5. **Output** — The answer is displayed in the Streamlit UI with expandable source page references.

---

## 💡 Example Usage

```
📄 Upload: "Annual_Report_2024.pdf"

You: What was the total revenue in 2024?

Bot: According to the document, the total revenue in 2024 was $8.6 billion,
     representing a 14% increase compared to the previous year, driven by
     strong growth in the enterprise software segment.
     [Source: Page 12, Page 13]
```

---

## 🧩 Configuration

Edit `config.py` to customize behaviour:

| Parameter | Default | Description |
|---|---|---|
| `CHUNK_SIZE` | `1000` | Characters per text chunk |
| `CHUNK_OVERLAP` | `200` | Overlap between consecutive chunks |
| `TOP_K` | `4` | Number of chunks retrieved per query |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | HuggingFace embedding model |
| `LLM_MODEL` | `gemini-2.5-flash` | Gemini model for generation |

---

## ☁️ Deploy to Streamlit Cloud

1. Push the repo to GitHub (make sure `.env` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **New app**
3. Connect your GitHub repo → set main file as `app.py`
4. Click **Advanced settings** → under **Secrets**, paste:

```toml
GOOGLE_API_KEY = "AIzaSy_your_key_here"
```

5. Click **Deploy** — your app will be live in ~2 minutes

> ✅ HuggingFace embeddings run locally inside the Streamlit Cloud container — no extra configuration needed.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<p align="center">Built with LangChain, HuggingFace, Gemini & ❤️ — 100% Free Stack</p>
