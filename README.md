# RAG_project
# 1. Librării necesare instalării
```bash
pip install langchain
pip install langchain-community
pip install langchain-core
pip install langchain-chroma
pip install langchain-ollama

pip install chromadb

pip install beautifulsoup4
pip install lxml

pip install python-dateutil

pip install langgraph
```

## Ollama

Este necesară instalarea Ollama:

https://ollama.com

Modelele utilizate în cadrul proiectului:

```bash
ollama pull qwen3:4b
ollama pull llama3.2:3b
ollama pull mistral
ollama pull bge-m3
```

---
# 2. Benchmark LLM

Au fost evaluate trei modele open-source.
"llama3.2:3b"
"mistral:latest"
"qwen3:4b"
Evaluarea a urmărit:

- timpul mediu de execuție pentru Planner;
- timpul mediu de execuție pentru Generator;
- calitatea QueryPlan-ului generat.

Scorul QueryPlan este calculat pe baza celor cinci componente generate:

- semantic_query
- sections
- date_filter
- sort
- analytics

Fiecare componentă corectă primește un punct.

Scor maxim:

```
5/5
```

## Rezultate

| Model | Average Planner (s) | Average Generator (s) | Total Time (s) | QueryPlan Score (/5) |
|--------|--------------------:|----------------------:|---------------:|---------------------:|
| Llama - Top News | 1.401 | 2.878 | 4.279 | 4 |
| Mistral - Top News | 1.964 | 7.482 | 9.446 | 4 |
| Qwen - Top News | 22.090 | 54.370 | 76.460 | 5 |
| Llama - OpenClaw | 1.314 | 2.621 | 3.935 | 5 |
| Mistral - OpenClaw | 1.521 | 8.661 | 10.182 | 5 |
| Qwen - OpenClaw | 35.928 | 57.610 | 93.538 | 5 |
| Llama - Likes | 1.623 | 2.778 | 4.401 | 4 |
| Mistral - Likes | 1.856 | 5.079 | 6.935 | 3 |
| Qwen - Likes | 25.968 | 35.367 | 61.334 | 5 |
## Observații

### Qwen3

A obținut cel mai bun scor al QueryPlan-ului.

Principalul dezavantaj îl reprezintă timpul foarte mare de execuție.

---

### Mistral

A produs rezultate apropiate de Llama, însă fără o îmbunătățire semnificativă a acurateții.

În același timp, timpul de execuție a fost mai mare.

Din acest motiv, modelul nu a fost păstrat în arhitectura finală.

---

### Llama3.2

A obținut cel mai mic timp de execuție.

Deși planner-ul nu generează întotdeauna un QueryPlan perfect, necesită optimizare.

Rămâne un posibil candidat.

---
