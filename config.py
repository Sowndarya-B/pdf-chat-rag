import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 4
LLM_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "models/embedding-001"