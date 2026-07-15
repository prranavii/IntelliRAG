from rag.query_engine import QueryEngine

engine = QueryEngine()

while True:

    question = input("\nAsk about the repository: ")

    if question.lower() == "exit":
        break

    result = engine.ask(question)

    print("\nAnswer:\n")
    print(result["answer"])

    print("\nSources:\n")

    for doc in result["documents"]:

        print(doc.metadata["filename"])