"""
Data Ingestion Module

This module handles the ingestion of documents into an Astra DB
vector store using Hugging Face embeddings. It supports loading
an existing vector store or creating a new one by ingesting data
from a CSV file.
"""

from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from src.data_converter import DataConverter
from src.config import Config


class DataIngestion:
    """
    Manages embedding creation and ingestion of documents
    into an Astra DB vector store.
    """

    def __init__(self):
        """
        Initialize the DataIngestion class.

        - Loads application configuration
        - Initializes the embedding model
        - Connects to the Astra DB vector store
        """
        self.config = Config()

        # Initialize embedding model
        self.embedding = HuggingFaceEndpointEmbeddings(
            model=self.config.EMBEDDING_MODEL
        )

        # Initialize Astra DB vector store
        self.vector_store = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name=self.config.COLLECTION_NAME,
            api_endpoint=self.config.ASTRA_DB_API_ENDPOINT,
            token=self.config.ASTRA_DB_APPLICATION_TOKEN,
            namespace=self.config.ASTRA_DB_KEYSPACE
        )

    def ingestion(self, load_existing: bool = True):
        """
        Load or create a vector store with embedded documents.

        Args:
            load_existing (bool): 
                If True, returns the existing vector store without
                re-ingesting documents. If False, ingests documents
                from the CSV file into the vector store.

        Returns:
            AstraDBVectorStore: Initialized vector store instance.
        """

        # Return existing vector store if ingestion is not required
        if load_existing is True:
            return self.vector_store

        # Convert CSV data into LangChain Document objects
        documents = DataConverter(
            file_path="data\\product_reviews.csv"
        ).convert()

        # Add documents to the vector store
        self.vector_store.add_documents(documents=documents)

        return self.vector_store
