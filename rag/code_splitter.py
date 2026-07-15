from langchain_text_splitters import RecursiveCharacterTextSplitter

code_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=150,
)


def split_code(documents):
    return code_splitter.split_documents(documents)