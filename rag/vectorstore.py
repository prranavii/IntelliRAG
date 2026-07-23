import chromadb
from pathlib import Path
from langchain_chroma import Chroma

from rag.embeddings import embeddings
from rag.config import CHROMA_DB_PATH


def create_vector_store(documents):
    # Ensure directory is created automatically
    Path(CHROMA_DB_PATH).mkdir(parents=True, exist_ok=True)

    # Clear Chroma system connection cache to prevent stale default_tenant locks
    chromadb.api.client.SharedSystemClient.clear_system_cache()

    client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))

    db = Chroma(
        client=client,
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
        client=client,
    )

    return db


def load_vector_store():
    # Ensure directory is created automatically
    Path(CHROMA_DB_PATH).mkdir(parents=True, exist_ok=True)

    chromadb.api.client.SharedSystemClient.clear_system_cache()

    client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))

    return Chroma(
        client=client,
        embedding_function=embeddings,
    )