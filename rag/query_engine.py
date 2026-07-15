from rag.retriever import get_retriever
from rag.prompt import PROMPT
from rag.llm import llm


class QueryEngine:

    def __init__(self):
        self.retriever = get_retriever()

    def ask(self, question: str):

        docs = self.retriever.invoke(question)

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        prompt = PROMPT.invoke(
            {
                "context": context,
                "question": question
            }
        )

        response = llm.invoke(prompt)

        return {
            "answer": response.content,
            "documents": docs
        }