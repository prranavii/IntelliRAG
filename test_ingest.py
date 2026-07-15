from rag.ingest import IngestionManager

manager = IngestionManager()

manager.ingest_github(
    "https://github.com/langchain-ai/langchain"
)