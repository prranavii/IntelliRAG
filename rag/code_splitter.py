from langchain_text_splitters import RecursiveCharacterTextSplitter

code_splitter = RecursiveCharacterTextSplitter(
    chunk_size=900,
    chunk_overlap=200,
    separators=[
        "\nclass ",
        "\ndef ",
        "\n\n",
        "\n",
        " ",
        ""
    ]
)


def split_code(documents):
    return code_splitter.split_documents(documents)