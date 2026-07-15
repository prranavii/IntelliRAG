from rag.vectorstore import load_vector_store


def get_retriever():

    db = load_vector_store()

    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    return retriever