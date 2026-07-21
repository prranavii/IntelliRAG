import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

CHROMA_DB_PATH = "chroma_db"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

LLM_MODEL = "llama-3.3-70b-versatile"