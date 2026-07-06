from collections import defaultdict
from analysis_models import DocumentAnalysis, AnalysisResult


def run_analysis(docs, plan) -> AnalysisResult:
    return run_trend_analysis(
        docs=docs,
        metric="likes",
        group_by="date",
    )


def run_trend_analysis(docs, metric: str, group_by: str) -> AnalysisResult:
    grouped = defaultdict(list)

    for doc in docs:
        metadata = doc.metadata
        print(metadata.get("section"), metadata.get("date"), metadata.get("likes"), type(metadata.get("likes")))
        group_value = metadata.get(group_by)
        metric_value = metadata.get(metric)

        if group_value is None or metric_value is None:
            continue

        if isinstance(metric_value, list):
            grouped[group_value].extend(metric_value)
        else:
            grouped[group_value].append(metric_value)

    rows = []

    for group_value, values in sorted(grouped.items()):
        documents = len(values)
        average = sum(values) / documents if documents else 0
        maximum = max(values) if values else 0
        total = sum(values) if values else 0

        rows.append(
            DocumentAnalysis(
                date=group_value,
                documents=documents,
                average=round(average, 2),
                maximum=maximum,
                percentage_increase=0,
                total=total,
            )
        )

    if not rows:
        return AnalysisResult(
            analysis_type="trend",
            metric=metric,
            baseline=None,
            rows=[],
        )

    baseline_total = rows[0].total

    for row in rows:
        if baseline_total:
            row.percentage_increase = round(
                ((row.total - baseline_total) / baseline_total) * 100,
                2,
            )
        else:
            row.percentage_increase = 0

    return AnalysisResult(
        analysis_type="trend",
        metric=metric,
        baseline=rows[0],
        rows=rows,
    )