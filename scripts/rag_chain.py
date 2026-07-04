from config import CHROMA_FOLDER, COLLECTION_NAME, EMBEDDING_MODEL, LLM_MODEL, TOP_K

from GAR import plan_query
from filter_generation import build_chroma_filter, get_retrieval_query

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate


def build_context(docs):
    context_parts = []

    for i, doc in enumerate(docs, start=1):
        metadata = doc.metadata
        print(doc.metadata)
        context_parts.append(
            f"""
DOCUMENT {i}
Section: {metadata.get("section")}
Date: {metadata.get("date")}
Source: {metadata.get("source_name")}
URL: {metadata.get("source_url")}
Likes: {metadata.get("likes")}

Content:
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
You are a RAG assistant.

Answer in Romanian.
Use only the provided context.
If the context contains partial information, summarize what is available.
Mention the available sources and URLs when relevant.

If the context does not contain relevant information, say:
"Nu am găsit informația în documentele indexate."

Context:
{context}

Question:
{question}
"""
    )

    query = input("Întrebare: ")

    plan = plan_query(query)
    metadata_filter = build_chroma_filter(plan)
    retrieval_query = get_retrieval_query(query, plan)

    print("\n=== QUERY PLAN ===")
    print(plan)

    print("\n=== CHROMA FILTER ===")
    print(metadata_filter)

    print("\n=== RETRIEVAL QUERY ===")
    print(retrieval_query)

    docs = vectorstore.similarity_search(
        retrieval_query,
        k=TOP_K,
        filter=metadata_filter,
    )

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