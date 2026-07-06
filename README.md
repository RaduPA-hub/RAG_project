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
# 2. Arhitectura soluției

Fluxul sistemului este împărțit în două etape:
## Arhitectura soluției

<p align="center">
  <img src="diagrams/architecture.svg" width="900">
</p>


1.Indexing ( executată o singură dată, la apariția unor documente noi )

Parserul extrage atât conținutul documentelor, cât și metadatele asociate acestora:

- secțiune;
- dată;
- număr de reacții (like-uri);
- URL;
- sursă (document);

Documentele sunt transformate în embedding-uri și indexate în ChromaDB.



### Query Planner

Planner-ul analizează întrebarea utilizatorului și generează un plan de interogare ce conține:

- semantic_query;
- sections;
- date_filter;
- analytics;
- sort.

Acest plan este utilizat pentru construirea interogării către ChromaDB.

---

### Retriever

Retriever-ul realizează căutarea semantică utilizând:

- embedding-ul întrebării;
- filtrele generate de Query Planner.

Rezultatul constă în primele K documente considerate relevante.

---

### Analyser

Pentru întrebările care solicită analiză statistică ( trend, engagement) se apeleaza acest tool si genereaza:
- totalul;
- media;
- valoarea maximă;
- creșterea procentuală.

---

### Answer Generator

Generatorul primește:

- întrebarea utilizatorului;
- documentele recuperate;
- rezultatul analizei (dacă există)

și generează răspunsul final.

---

---
# 3. Benchmark LLM

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
# 4. Evaluarea Retrieval-ului

Au fost comparate trei strategii diferite de retrieval:

- Retrieval Vanilla;
- Retrieval If-Based ( generarea planului de interogare cu if-uri explicite, fără utilizarea unui LLM );
- Retrieval asistat de GAR.

Rezultatele au arătat că, pentru dimensiunea actuală a colecției de documente, Retrieval If-Based și GAR oferă performanțe comparabile din punctul de vedere al documentelor recuperate, ambele depășind Retrieval Vanilla în scenariile bazate pe filtrarea metadatelor.

În cazul interogărilor semantice complexe, planner-ul GAR oferă avantajul interpretării întrebării utilizatorului și generării automate a unei interogări semantice și a filtrelor necesare retrieval-ului.

---

# 5. Limitări

Fiind un Proof of Concept, sistemul prezintă câteva limitări:

- compatibil doar cu surse de informare in format HTML;
- retrieval-ul este bazat exclusiv pe semantic search;
- nu este implementat încă un mecanism de reranking;
- compromis semnificativ între acuratețe și timp de execuție

---

# 6. Dezvoltări viitoare

Direcțiile de dezvoltare planificate includ:

- Hybrid Retrieval;
- Cross-Encoder Reranking;
- optimizarea generării semantic_query ( pentru llama );
- extinderea metadatelor disponibile;
- suport pentru noi tipuri de documente;