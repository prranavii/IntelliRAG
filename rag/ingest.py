from rag.loaders import DocumentLoader
from rag.code_splitter import split_code
from rag.github_reader import load_repository
from rag.splitter import split_documents
from rag.vectorstore import create_vector_store

from utils.github_loader import GitHubLoader


class IngestionManager:

    def ingest_pdf(self, folder="data/pdfs"):

        docs = DocumentLoader.load_pdf(folder)

        chunks = split_code(docs)

        create_vector_store(chunks)

        print(f"Indexed {len(chunks)} PDF chunks.")

    def ingest_github(self, github_url):

        loader = GitHubLoader()

        repo_path = loader.clone_repo(github_url)

        docs = load_repository(repo_path)

        chunks = split_documents(docs)

        create_vector_store(chunks)

        print(f"Indexed {len(chunks)} GitHub chunks.")