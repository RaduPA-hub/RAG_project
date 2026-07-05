from dataclasses import dataclass


@dataclass
class DocumentAnalysis:
    date: str
    documents: int
    average: float
    maximum: int
    percentage_increase: float


@dataclass
class AnalysisResult:
    analysis_type: str
    metric: str
    baseline: DocumentAnalysis | None
    rows: list[DocumentAnalysis]