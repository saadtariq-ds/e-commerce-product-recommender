"""
Data Conversion Module

This module provides a utility class for converting CSV data
into LangChain Document objects for downstream processing
(e.g., embeddings, vector stores, or RAG pipelines).
"""

import pandas as pd
from typing import List
from langchain_core.documents import Document

class DataConverter:
    """
    Converts structured CSV data into LangChain Document objects.

    Each row in the CSV is transformed into a Document where:
    - `review` becomes the document content
    - `product_title` is stored as metadata
    """
    def __init__(self, file_path:str):
        """
        Initialize the DataConverter.

        Args:
            file_path (str): Path to the CSV file containing product reviews.
        """
        self.file_path = file_path

    def convert(self) -> List[Document]:
        """
        Convert CSV rows into a list of LangChain Document objects.

        Returns:
            list[Document]: List of Document objects created from the CSV data.
        """
        # Read CSV file and select required columns
        df = pd.read_csv(self.file_path)[["product_title", "review"]]

        # Convert each row into a LangChain Document
        documents = [
            Document(page_content=row["review"], metadata={"product_name":row["product_title"]})
            for _, row in df.iterrows()
        ]

        return documents