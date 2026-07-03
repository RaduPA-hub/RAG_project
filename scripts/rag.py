from config import CHROMA_FOLDER, COLLECTION_NAME, EMBEDDING_MODEL, LLM_MODEL, TOP_K

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate


def build_context(docs):
    context_parts = []

    for i, doc in enumerate(docs, start=1):
        metadata = doc.metadata

        source = metadata.get("source_name", "unknown source")
        section = metadata.get("section", "unknown")
        url = metadata.get("source_url", None)
        timestamp = metadata.get("timestamp", None)

        context_parts.append(
            f"""
[SOURCE {i}]
Section: {section}
Source: {source}
URL: {url}
Timestamp: {timestamp}
{doc.page_content}
"""
        )

    return "\n\n".join(context_parts)


def main():
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    vectorstore = Chroma(
        persist_directory=CHROMA_FOLDER,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )

    llm = ChatOllama(model=LLM_MODEL, temperature=0)

    prompt = ChatPromptTemplate.from_template(
        """
You are a RAG assistant. Answer only using the provided context.
If the answer is partly contained, provide the best possible answer based on the context.
If the answer is not present in the context, say:
"Nu am găsit informația în documentele indexate."

Answer in Romanian.

Context:
{context}

Question:
{question}
"""
    )

    query = input("Întrebare: ")

    docs = vectorstore.similarity_search(query, k=TOP_K)

    print(f"\nRetrieved {len(docs)} documents.")

    context = build_context(docs)

    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "question": query,
        }
    )

    print("\n=== RĂSPUNS ===\n")
    print(response.content)


if __name__ == "__main__":
    main()