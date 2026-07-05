import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import time
from config import LLM_MODEL
from query_plan import QueryPlan


PLANNER_PROMPT = """
You are a retrieval planner for a RAG system.
/no_think
Return ONLY valid JSON. Do not add explanations.

Available metadata:

section:
- article
- top_news
- top_paper
- signals
- sponsored

Available date filters:
- last_day
- last_week
- last_month

Available sort:
- likes
- timestamp

Return this JSON structure:

{{
  "semantic_query": "",
  "sections": [],
  "date_filter": null,
  "sort": null,
  "analytics": false
}}

Rules:
- If the question asks for more information about a topic, use article and top_news and top_paper and sponsored.
- If the question asks about evolution, trend or any math related questions regarding likes or reactions, or romanian equivalent, set analytics to true.
- If the question mentions ultima săptămână / last week, use "last_week".
- If the question mentions ultima lună / last month, use "last_month".
- If the question mentions ultima zi / last day, use "last_day".
- semantic_query must be short, at most two words.
- semantic_query should contain only the main entity/topic that the information is requested about, not the action, not the whole question.
- semantic_query must be in English, even if the question is in Romanian, you should translate it to English.
- Do NOT return generic domains such as:
  - AI
  - Artificial Intelligence
  - Machine Learning
  - LLM
  - Deep Learning
  - Technology
- If the question only refers to a generic category (e.g. "Top AI news"), semantic_query must be an empty string "".
- If no specific entity exists, semantic_query must be "".
- If the question contains  day, week, month or romanian equivalent, set sort to "timestamp".
- If the question contains reactions, likes, popularity, engagement or romanian equivalent, set sort to "likes", even over timestamp being selected.

User question:
{question}

"""


import time

def plan_query(question: str) -> QueryPlan:
    t0 = time.perf_counter()

    llm = ChatOllama(
        model=LLM_MODEL,
        temperature=0,
    )
    t1 = time.perf_counter()

    prompt = ChatPromptTemplate.from_template(PLANNER_PROMPT)
    t2 = time.perf_counter()

    chain = prompt | llm
    t3 = time.perf_counter()
    formatted = prompt.format(question=question)

    print("=" * 80)
    print(formatted)
    print("=" * 80)
    print(len(formatted))
    response = chain.invoke({"question": question})
    t4 = time.perf_counter()

    raw = response.content.strip()
    t5 = time.perf_counter()

    data = json.loads(raw)
    t6 = time.perf_counter()

    plan = QueryPlan(
        semantic_query=data.get("semantic_query", ""),
        sections=data.get("sections", []),
        date_filter=data.get("date_filter"),
        sort=data.get("sort"),
        analytics=data.get("analytics", False),
    )
    t7 = time.perf_counter()
    print(response.content)
    print(response.response_metadata)
    print(f"LLM init      : {t1-t0:.3f}s")
    print(f"Prompt build  : {t2-t1:.3f}s")
    print(f"Chain build   : {t3-t2:.3f}s")
    print(f"Invoke        : {t4-t3:.3f}s")
    print(f"Strip         : {t5-t4:.6f}s")
    print(f"JSON          : {t6-t5:.6f}s")
    print(f"QueryPlan     : {t7-t6:.6f}s")
    return plan 
if __name__ == "__main__":
    question = input("Întrebare: ")
    plan = plan_query(question)

    print("\n=== QUERY PLAN ===")
    print(plan)