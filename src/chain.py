"""
RAG Chain Builder Module

This module defines the RAGChainBuilder class, which builds a history-aware
retrieval-augmented generation (RAG) chain using:
- Astra DB (or any LangChain-compatible vector store retriever)
- Groq LLM via ChatGroq
- Message history for conversational memory
"""

from langchain_groq import ChatGroq
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from src.config import Config
from src.prompts import RAG_CONTEXT_REWRITE_SYSTEM_PROMPT, RAG_QA_SYSTEM_PROMPT

class RAGChainBuilder:
    """
    Builds a conversational RAG pipeline with message history support.

    Features:
    - Uses a vector store retriever to fetch top-k relevant documents.
    - Rewrites the user question into a standalone query using chat history.
    - Answers the question using retrieved documents as context.
    - Maintains chat history per session_id.
    """
    def __init__(self, vector_store):
        """
        Initialize the RAG chain builder.

        Args:
            vector_store: Any LangChain-compatible vector store instance
                         that supports `.as_retriever()`.
        """
        self.config = Config()
        self.vector_store = vector_store

        # Initialize the LLM used for both question rewriting and answering
        self.model = ChatGroq(model=self.config.LLM_MODEL , temperature=0.5)

        # In-memory store for chat histories keyed by session_id
        self.history_store = {}

    def _get_history(self,session_id:str) -> BaseChatMessageHistory:
        """
        Retrieve (or create) chat history for the given session ID.

        Args:
            session_id (str): Unique identifier for a user session.

        Returns:
            BaseChatMessageHistory: Chat history object used by LangChain.
        """
        if session_id not in self.history_store:
            # Create a new chat history if one doesn't exist for this session
            self.history_store[session_id] = ChatMessageHistory()

        return self.history_store[session_id]
    
    def build_chain(self) -> RunnableWithMessageHistory:
        """
        Build and return a history-aware RAG chain wrapped with message history.

        Returns:
            RunnableWithMessageHistory: A runnable chain that tracks chat history.
        """
        # Create retriever from vector store (top-k results)
        retriever = self.vector_store.as_retriever(
            search_kwargs={"k":3}
        )

        # Prompt to convert a history-dependent question into a standalone query
        context_prompt = ChatPromptTemplate.from_messages([
            ("system", RAG_CONTEXT_REWRITE_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])

        # Prompt used to answer the user's question using retrieved context
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", RAG_QA_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])

        # Create a retriever that first rewrites the question using chat history
        history_aware_retriever = create_history_aware_retriever(
            llm=self.model,
            retriever=retriever, 
            prompt=context_prompt
        )

        # Create question-answering chain that "stuffs" retrieved documents into context
        question_answer_chain = create_stuff_documents_chain(
            llm=self.model,
            prompt=qa_prompt
        )

        # Create full retrieval chain: retrieve docs -> answer using docs
        rag_chain = create_retrieval_chain(
            retriever=history_aware_retriever,
            combine_docs_chain=question_answer_chain
        )

        # Wrap chain with message history handling per session
        return RunnableWithMessageHistory(
            rag_chain,
            self._get_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

