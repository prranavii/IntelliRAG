from langchain_chroma import Chroma

from rag.embeddings import embeddings
from rag.config import CHROMA_DB_PATH


def create_vector_store(documents):

    db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH,
    )

    return db


def load_vector_store():

    return Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings,
    )