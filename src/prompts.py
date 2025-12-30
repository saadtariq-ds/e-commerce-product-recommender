"""
Prompt templates for the RAG pipeline.

This file centralizes prompt strings so they can be reused and updated
without modifying chain-building logic.
"""

# Prompt used to rewrite a user's question into a standalone query
# using chat history as additional context.
RAG_CONTEXT_REWRITE_SYSTEM_PROMPT = (
    "Given the chat history and user question, rewrite it as a standalone question."
)

# Prompt used for final question answering using retrieved context.
RAG_QA_SYSTEM_PROMPT = """
You're an e-commerce bot answering product-related queries using reviews and titles.
Stick to context. Be concise and helpful.

CONTEXT:
{context}

QUESTION: {input}
"""
