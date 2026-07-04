from pathlib import Path
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from config import DATA_FOLDER
import re
from dateutil import parser as date_parser


def extract_first_link(table):
    link = table.find("a", href=True)
    if link:
        return link["href"]
    return None


def detect_section(text: str) -> str:
    text_lower = text.lower().strip()

    if text_lower.startswith("summary") or "read time:" in text_lower:
        return "summary"

    if text_lower.startswith("signals"):
        return "signals"

    if text_lower.startswith("top news"):
        return "top_news"

    if text_lower.startswith("top paper"):
        return "top_paper"

    if text_lower.startswith("presented by"):
        return "sponsored"
    
    if "likes" in text_lower:
        return "article"

    return "other"

def extract_document_timestamp(soup):
    tables = soup.find_all("table")

    if not tables:
        return None, None

    rows = tables[0].find_all("tr")

    if len(rows) < 2:
        return None, None

    raw = rows[1].get_text(" ", strip=True)
    raw = raw.replace("Sent:", "").strip()


    try:
        parsed_date = date_parser.parse(raw).date()
        return parsed_date.isoformat(), parsed_date.toordinal()
    except Exception:
        return None, None


def extract_likes(text: str):
    match = re.search(r"([\d,]+)\s+Likes", text)
    if match:
        return int(match.group(1).replace(",", ""))
    return None

def load_table_documents():
    html_files = list(DATA_FOLDER.glob("*.html"))
    documents = []

    for html_file in html_files:
        html = html_file.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(html, "lxml")
        date, date_ordinal = extract_document_timestamp(soup)
        tables = soup.find_all("table")

        for table_index, table in enumerate(tables):
            text = table.get_text("\n", strip=True)

            if len(text) < 30:
                continue

            # primul tabel = From / Sent / To / Subject
            if table_index == 0:
                continue

            section = detect_section(text)

            # nu indexăm summary-ul, pentru că domină retrieval-ul
            if section == "summary":
                continue

            source_url = extract_first_link(table)

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": str(html_file),
                        "source_name": html_file.name,
                        "table_index": table_index,
                        "section": section,
                        "source_url": source_url,
                        "date": date,
                        "date_ordinal": date_ordinal,
                        "likes": extract_likes(text),
                    },
                )
            )

    return documents


if __name__ == "__main__":
    docs = load_table_documents()

    print(f"Documents created: {len(docs)}")

    for i, doc in enumerate(docs[:10], start=1):
        print(f"\n--- TABLE CHUNK {i} ---")
        print(doc.metadata)
        print(doc.page_content[:500])