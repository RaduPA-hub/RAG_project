from config import CHROMA_FOLDER, COLLECTION_NAME, EMBEDDING_MODEL
from parser import load_table_documents

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


def main():
    documents = load_table_documents()

    print(f"Documents loaded: {len(documents)}")
    print(f"Embedding model: {EMBEDDING_MODEL}")

    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url="http://127.0.0.1:11434",
    )

    print("Testing embedding...")
    vec = embeddings.embed_query("Hello world")
    print(f"Embedding dimensions: {len(vec)}")

    vectorstore = Chroma(
        persist_directory=CHROMA_FOLDER,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )

    batch_size = 16

    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        vectorstore.add_documents(batch)
        print(f"Indexed {i + len(batch)}/{len(documents)}")

    print("ChromaDB index created successfully.")
    print(f"Persisted in: {CHROMA_FOLDER}")


if __name__ == "__main__":
    main()