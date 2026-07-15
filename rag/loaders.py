from langchain_community.document_loaders import PyPDFDirectoryLoader


class DocumentLoader:

    @staticmethod
    def load_pdf(folder_path: str):
        loader = PyPDFDirectoryLoader(folder_path)
        return loader.load()