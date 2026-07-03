from config import CHROMA_FOLDER, COLLECTION_NAME, EMBEDDING_MODEL, TOP_K
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


def main():
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    vectorstore = Chroma(
        persist_directory=CHROMA_FOLDER,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )

    query = "Vreau mai multe informatii despre OpenClaw"

    results = vectorstore.similarity_search_with_score(
        query,
        k=TOP_K
    )

    print(f"Query: {query}")
    print(f"Results: {len(results)}")

    for i, (doc, score) in enumerate(results, start=1):
        print(f"\n--- RESULT {i} ---")
        print(f"Score: {score}")
        print(f"Metadata: {doc.metadata}")
        print(doc.page_content[:1000])


if __name__ == "__main__":
    main()