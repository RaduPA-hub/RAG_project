import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from config import LLM_MODEL
from query_plan import QueryPlan


PLANNER_PROMPT = """
You are a retrieval planner for a RAG system.

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
- If the question asks about evolution, trend, reactions or likes, set analytics to true.
- If the question mentions ultima săptămână / last week, use "last_week".
- If the question mentions ultima lună / last month, use "last_month".
- If the question mentions ultima zi / last day, use "last_day".
- semantic_query must be short.
- semantic_query should contain only the main entity/topic that the information is requested about, not the action, not the whole question.
- semnatic_query must be in English, even if the question is in Romanian, you should translate it to English.
- If the semantic_query is an abreviation, you should expand it to the full name in English.
- If the question contains  day, week, month or romanian equivalent, set sort to "timestamp".
- If the question contains reactions, likes, popularity, engagement or romanian equivalent, set sort to "likes", even over timestamp being selected.

User question:
{question}

"""


def plan_query(question: str) -> QueryPlan:
    llm = ChatOllama(model=LLM_MODEL, temperature=0)

    prompt = ChatPromptTemplate.from_template(PLANNER_PROMPT)
    chain = prompt | llm

    response = chain.invoke({"question": question})

    raw = response.content.strip()

    data = json.loads(raw)
    return QueryPlan(
        semantic_query=data.get("semantic_query", ""),
        sections=data.get("sections", []),
        date_filter=data.get("date_filter"),
        sort=data.get("sort"),
        analytics=data.get("analytics", False)
    )

if __name__ == "__main__":
    question = input("Întrebare: ")
    plan = plan_query(question)

    print("\n=== QUERY PLAN ===")
    print(plan)