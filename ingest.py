from rag.loaders import DocumentLoader
from rag.splitter import split_documents
from rag.vectorstore import create_vector_store


print("Loading PDFs...")

docs = DocumentLoader.load_pdf("data/pdfs")

print(f"Loaded {len(docs)} pages.")

chunks = split_documents(docs)

print(f"Created {len(chunks)} chunks.")

db = create_vector_store(chunks)

print("✅ Chroma Vector Database Created Successfully!")