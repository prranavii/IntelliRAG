from rag.chain import get_rag_chain

chain = get_rag_chain()

while True:

    question = input("\nAsk: ")

    if question.lower() == "exit":
        break

    response = chain.invoke(
        {"input": question}
    )

    print("\nAnswer:\n")

    print(response["answer"])