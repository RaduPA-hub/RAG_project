from pathlib import Path

DATA_FOLDER = Path("data sources")

CHROMA_FOLDER = "chroma_db"
COLLECTION_NAME = "newsletter_chunks"

EMBEDDING_MODEL = "bge-m3"
LLM_MODEL = "qwen3:4b"

TOP_K = 15