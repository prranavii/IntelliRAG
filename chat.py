from rag.query_engine import QueryEngine

engine = QueryEngine()

print("=" * 50)
print("Welcome to IntelliRAG")
print("Type 'exit' to quit.")
print("=" * 50)

while True:

    question = input("\nAsk: ")

    if question.lower() == "exit":
        break

    result = engine.ask(question)

    print("\nAnswer:\n")
    print(result["answer"])

    print("\nRetrieved Documents:\n")

    for i, doc in enumerate(result["documents"], 1):

        print(f"[{i}] {doc.metadata.get('source')}")