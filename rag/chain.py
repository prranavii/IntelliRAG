from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

from rag.llm import llm
from rag.retriever import get_retriever


prompt = ChatPromptTemplate.from_template(
    """
You are an expert AI assistant.

Answer ONLY from the provided context.

If the answer isn't available in the context, say:

"I couldn't find this information in the knowledge base."

<context>
{context}
</context>

Question:
{input}
"""
)


def get_rag_chain():

    retriever = get_retriever()

    document_chain = create_stuff_documents_chain(
        llm,
        prompt
    )

    chain = create_retrieval_chain(
        retriever,
        document_chain
    )

    return chain