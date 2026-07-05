from GAR import plan_query
from filter_generation import build_chroma_filter, get_retrieval_query
from retriver import retrieve_documents
from response import generate_answer

from config import TOP_K


def main():
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

    docs = retrieve_documents(
        query=retrieval_query,
        metadata_filter=metadata_filter,
        k=TOP_K,
    )

    print(f"\nRetrieved {len(docs)} documents.")

    response = generate_answer(query, docs)

    print("\n=== RĂSPUNS ===\n")
    print(response)


if __name__ == "__main__":
    main()