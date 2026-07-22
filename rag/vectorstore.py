from pathlib import Path
from langchain_chroma import Chroma

from rag.embeddings import embeddings
from rag.config import CHROMA_DB_PATH


def create_vector_store(documents):
    # Ensure directory is created automatically
    Path(CHROMA_DB_PATH).mkdir(parents=True, exist_ok=True)

    db = Chroma(
        persist_directory=str(CHROMA_DB_PATH),
        embedding_function=embeddings,
    )

    # Delete old collection
    try:
        db.delete_collection()
    except Exception:
        pass

    # Create fresh collection
    db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_PATH),
    )

    return db


def load_vector_store():
    # Ensure directory is created automatically
    Path(CHROMA_DB_PATH).mkdir(parents=True, exist_ok=True)

    return Chroma(
        persist_directory=str(CHROMA_DB_PATH),
        embedding_function=embeddings,
    )