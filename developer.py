from rag.ingest import IngestionManager
from rag.query_engine import QueryEngine

manager = IngestionManager()
engine = QueryEngine()

while True:

    print("\n" + "=" * 50)
    print("IntelliRAG Developer Console")
    print("=" * 50)

    print("1. Ingest PDFs")
    print("2. Ingest GitHub Repository")
    print("3. Chat with Knowledge Base")
    print("4. Exit")

    choice = input("\nSelect Option: ")

    if choice == "1":

        manager.ingest_pdf("data/pdfs")

    elif choice == "2":

        github_url = input("\nGitHub URL: ")

        manager.ingest_github(github_url)

    elif choice == "3":

        while True:

            question = input("\nQuestion (type 'back' to return): ")

            if question.lower() == "back":
                break

            result = engine.ask(question)

            print("\nAnswer:\n")

            print(result["answer"])

            print("\nSources:\n")

            for doc in result["documents"]:

                print(
                    f"{doc.metadata.get('filename')} "
                    f"({doc.metadata.get('extension')})"
                )

    elif choice == "4":

        print("Goodbye!")

        break

    else:

        print("Invalid Choice.")