from datetime import date, timedelta
from query_plan import QueryPlan


def resolve_date_filter(date_filter: str | None):
    if not date_filter:
        return None

    #today = date.today()
    today = date(2026, 4, 5).toordinal()
    if date_filter == "last_day":
        return today - 1

    if date_filter == "last_week":
        return today - 7

    if date_filter == "last_month":
        return today - 30

    return None


def build_chroma_filter(plan: QueryPlan):
    filters = []

    if plan.sections:
        filters.append({
            "section": {
                "$in": plan.sections
            }
        })

    start_date = resolve_date_filter(plan.date_filter)

    if start_date:
        filters.append({
            "date_ordinal": {
                "$gte": start_date
            }
        })

    if not filters:
        return None

    return filters[0] if len(filters) == 1 else {"$and": filters}


def get_retrieval_query(user_query: str, plan: QueryPlan):
    return plan.semantic_query or user_query