from dataclasses import dataclass

@dataclass
class QueryPlan:

    semantic_query: str

    sections: list[str]

    date_filter: str | None

    sort: str | None

    analytics: bool