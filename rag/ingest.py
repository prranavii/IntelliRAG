from rag.loaders import DocumentLoader
from rag.code_splitter import split_code
from rag.github_reader import load_repository
from rag.splitter import split_documents
from rag.vectorstore import create_vector_store

from utils.github_loader import GitHubLoader
from rag.website_loader import load_website


class IngestionManager:

    def ingest_pdf(self, folder="data/pdfs"):

        docs = DocumentLoader.load_pdf(folder)

        chunks = split_documents(docs)

        create_vector_store(chunks)

        print(f"Indexed {len(chunks)} PDF chunks.")
        return len(chunks)

    def ingest_github(self, github_url):

        loader = GitHubLoader()

        repo_path = loader.clone_repo(github_url)

        docs = load_repository(repo_path)

        chunks = split_documents(docs)

        create_vector_store(chunks)

        print(f"Indexed {len(chunks)} GitHub chunks.")
        return len(chunks)
    
    def ingest_website(self, url):

        docs = load_website(url)

        chunks = split_documents(docs)

        create_vector_store(chunks)

        print(f"Indexed {len(chunks)} Website chunks.")

        return len(chunks)

# docs = DocumentLoader.load_pdf(folder)

# print("=" * 50)
# print("DOCUMENTS LOADED:", len(docs))

# for doc in docs:
#     print(doc.metadata)