import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

CHROMA_DB_PATH = "chroma_db"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

LLM_MODEL = "llama-3.3-70b-versatile"