from rag.github_reader import load_repository

docs = load_repository(
    "data/repos/langchain"
)

print(len(docs))

print(docs[0].metadata)

print(docs[0].page_content[:500])