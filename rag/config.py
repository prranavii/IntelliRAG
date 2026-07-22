import os
import platform
import tempfile
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "llama-3.3-70b-versatile"

# Cross-platform writable directories
if platform.system() == "Windows":
    CHROMA_DB_PATH = Path("chroma_db")
    UPLOAD_DIR = Path("data/uploads")
    REPOS_DIR = Path("data/repos")
    WEBSITES_DIR = Path("data/websites")
else:
    # On Linux (Streamlit Cloud, Render, Railway), use system temp directory to ensure writability
    temp_base = Path(tempfile.gettempdir())
    CHROMA_DB_PATH = temp_base / "chroma_db"
    UPLOAD_DIR = temp_base / "data" / "uploads"
    REPOS_DIR = temp_base / "data" / "repos"
    WEBSITES_DIR = temp_base / "data" / "websites"