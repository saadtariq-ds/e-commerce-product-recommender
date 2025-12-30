"""
Application Configuration Module

This module loads and centralizes environment-based configuration
variables used across the application, such as database credentials,
API keys, and model settings.
"""

import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    """
    Central configuration class for the application.

    All configuration values are loaded from environment variables
    to keep secrets and environment-specific settings out of the codebase.
    """
    # Astra DB configuration
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")

    # Astra DB Database
    COLLECTION_NAME = "e_commerce_database"

    # Groq API configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Model configuration
    EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
    LLM_MODEL = "llama-3.1-8b-instant"