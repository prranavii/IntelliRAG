from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = ChatPromptTemplate.from_template(
"""
You are IntelliRAG, an expert AI assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context, reply:

"I couldn't find that information in the indexed documents."

Context:
{context}

Question:
{question}
"""
)