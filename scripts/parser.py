from pathlib import Path
from bs4 import BeautifulSoup
from langchain_core.documents import Document

DATA_FOLDER = Path("data sources")
html_files = list(DATA_FOLDER.glob("*.html"))

first_file = html_files[2]
html = first_file.read_text(encoding="utf-8", errors="ignore")
soup = BeautifulSoup(html, "lxml")

tables = soup.find_all("table")

documents = []

for i, table in enumerate(tables):
    text = table.get_text("\n", strip=True)

    if len(text) < 30:
        continue

    doc = Document(
        page_content=text,
        metadata={
            "source": str(first_file),
            "source_name": first_file.name,
            "table_index": i,
            "chunk_number": len(documents) + 1
        }
    )

    documents.append(doc)

print(f"Tables found: {len(tables)}")
print(f"Documents created: {len(documents)}")

for i, doc in enumerate(documents, start=1):
    print(f"\n--- TABLE CHUNK {i} ---")
    print(doc.metadata)
    print(doc.page_content)