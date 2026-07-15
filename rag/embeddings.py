from langchain_huggingface import HuggingFaceEmbeddings
from rag.config import EMBEDDING_MODEL

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)