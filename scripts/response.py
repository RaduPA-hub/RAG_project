from dataclasses import asdict, is_dataclass

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from config import LLM_MODEL


def build_context(docs):
    context_parts = []

    for i, doc in enumerate(docs, start=1):
        metadata = doc.metadata

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


def serialize_analysis_result(analysis_result):
    if analysis_result is None:
        return ""

    if is_dataclass(analysis_result):
        return str(asdict(analysis_result))

    return str(analysis_result)


def generate_answer(question: str, docs=None, analysis_result=None):
    docs = docs or []

    llm = ChatOllama(
        model=LLM_MODEL,
        temperature=0,
        base_url="http://127.0.0.1:11434",
    )

    if analysis_result is not None:
        prompt = ChatPromptTemplate.from_template(
            """
You are an analytics assistant.

Answer in Romanian.
Use only the provided analysis result.
Explain the trend clearly.
Mention total, average, maximum and percentage increase when available, translate to Romanian.

Analysis result:
{analysis_result}

Question:
{question}
"""
        )

        chain = prompt | llm

        response = chain.invoke(
            {
                "analysis_result": serialize_analysis_result(analysis_result),
                "question": question,
            }
        )
        print(response.response_metadata)
        return response.content

    prompt = ChatPromptTemplate.from_template(
        """
You are a RAG assistant.

Rules:

1. Respond ONLY in Romanian.
2. Do not generate English explanations.
3. Keep article titles exactly as they appear.
4. Keep company names unchanged.
5. Keep URLs unchanged.
6. Translate all generated text to Romanian.
7. If the context is insufficient, explicitly say:
"Nu am găsit informația în documentele indexate."
8. Offer the variables requested on top of the analytical result if available.


Context:
{context}

Question:
{question}
"""
    )

    context = build_context(docs)
    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    return response.content