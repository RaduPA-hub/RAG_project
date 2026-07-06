from typing import TypedDict, Any
import time
from langgraph.graph import StateGraph, END

from GAR import plan_query
from filter_generation import build_chroma_filter, get_retrieval_query
from retriver import retrieve_documents
from response import generate_answer
from analysis import run_analysis

from config import TOP_K


class RAGState(TypedDict, total=False):
    question: str
    plan: Any
    metadata_filter: dict | None
    retrieval_query: str
    docs: list
    analysis_result: Any
    answer: str
    start_time: float


def planning_node(state: RAGState):
    question = state["question"]

    plan = plan_query(question)
    metadata_filter = build_chroma_filter(plan)
    retrieval_query = get_retrieval_query(question, plan)
    print(
        f"[Planner] {time.perf_counter()-state['start_time']:.3f}s"
    )
    return {
        "plan": plan,
        "metadata_filter": metadata_filter,
        "retrieval_query": retrieval_query,
    }


def retrieval_node(state: RAGState):
    docs = retrieve_documents(
        query=state["retrieval_query"],
        metadata_filter=state["metadata_filter"],
        k=TOP_K,
    )
    print(
        f"[Retriever] {time.perf_counter()-state['start_time']:.3f}s"
    )
    return {
        "docs": docs
    }


def route_after_retrieval(state: RAGState):
    plan = state["plan"]

    if plan.analytics:
        return "analysis"

    return "answer"


def analysis_node(state: RAGState):
    analysis_result = run_analysis(
        docs=state["docs"],
        plan=state["plan"],
    )
    print(
    f"[Analysis] {time.perf_counter()-state['start_time']:.3f}s"
    )
    return {
        "analysis_result": analysis_result
    }


def analysis_answer_node(state: RAGState):
    question = state["question"]
    analysis_result = state["analysis_result"]

    answer = generate_answer(
        question=question,
        docs=[],
        analysis_result=analysis_result,
    )
    print(
    f"[Generator] {time.perf_counter()-state['start_time']:.3f}s"
)
    return {
        "answer": answer
    }


def answer_node(state: RAGState):
    answer = generate_answer(
        question=state["question"],
        docs=state["docs"],
    )

    print(
        f"[Generator] {time.perf_counter()-state['start_time']:.3f}s"
    )
    return {
        "answer": answer
    }


def build_graph():
    graph = StateGraph(RAGState)

    graph.add_node("planning", planning_node)
    graph.add_node("retrieval", retrieval_node)
    graph.add_node("analysis", analysis_node)
    graph.add_node("analysis_answer", analysis_answer_node)
    graph.add_node("answer", answer_node)

    graph.set_entry_point("planning")

    graph.add_edge("planning", "retrieval")

    graph.add_conditional_edges(
        "retrieval",
        route_after_retrieval,
        {
            "analysis": "analysis",
            "answer": "answer",
        },
    )

    graph.add_edge("analysis", "analysis_answer")
    graph.add_edge("analysis_answer", END)

    graph.add_edge("answer", END)

    return graph.compile()


def print_debug(result):
    print("\n=== QUERY PLAN ===")
    print(result.get("plan"))

    print("\n=== CHROMA FILTER ===")
    print(result.get("metadata_filter"))

    print("\n=== RETRIEVAL QUERY ===")
    print(result.get("retrieval_query"))

    print(f"\nRetrieved {len(result.get('docs', []))} documents.")

    if result.get("analysis_result"):
        print("\n=== ANALYSIS RESULT ===")
        print(result.get("analysis_result"))


def main():
    app = build_graph()

    while True:
        question = input("\nÎntrebare: ")

        if question.lower().strip() in ["exit", "quit"]:
            break

        result = app.invoke(
            {
                "question": question,
                "start_time": time.perf_counter(),
            }
        )

        print_debug(result)

        print("\n=== RĂSPUNS ===\n")
        print(result["answer"])


if __name__ == "__main__":
    main()