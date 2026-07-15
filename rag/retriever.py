from rag.vectorstore import load_vector_store


def get_retriever():

    vectorstore = load_vector_store()

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 4
        }
    )