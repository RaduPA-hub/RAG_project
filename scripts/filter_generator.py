import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from config import LLM_MODEL


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
- If the question asks for more information about a topic, use article and top_news and top_paper.
- If the question asks about evolution, trend, reactions or likes, set analytics to true.
- If the question mentions ultima săptămână / last week, use "last_week".
- If the question mentions ultima lună / last month, use "last_month".
- If the question mentions ultima zi / last day, use "last_day".
- semantic_query must be short.
- semantic_query should contain only the main entity/topic that the information is requested about, not the action, not the whole question.
- If the question contains  day, week, month or romanian equivalent, set sort to "timestamp".
- If the question contains reactions, likes, popularity, engagement or romanian equivalent, set sort to, even over timestamp being selected "likes".

User question:
{question}

"""


def plan_query(question: str) -> dict:
    llm = ChatOllama(model=LLM_MODEL, temperature=0)

    prompt = ChatPromptTemplate.from_template(PLANNER_PROMPT)
    chain = prompt | llm

    response = chain.invoke({"question": question})

    raw = response.content.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print("Planner returned invalid JSON:")
        print(raw)
        raise


if __name__ == "__main__":
    question = input("Întrebare: ")
    plan = plan_query(question)

    print("\n=== QUERY PLAN ===")
    print(json.dumps(plan, indent=2, ensure_ascii=False))