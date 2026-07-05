from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from config import CHROMA_FOLDER, COLLECTION_NAME, EMBEDDING_MODEL, TOP_K


def get_vectorstore():
    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
    )

    return Chroma(
        persist_directory=CHROMA_FOLDER,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )


def retrieve_documents(query: str, metadata_filter=None, k: int = TOP_K):
    vectorstore = get_vectorstore()

    docs = vectorstore.similarity_search(
        query,
        k=k,
        filter=metadata_filter,
    )

    print("\n=== RETRIEVED DOC METADATA ===")
    for i, doc in enumerate(docs, start=1):
        print(f"\nDOC {i}")
        print(doc.metadata)

    return docs
