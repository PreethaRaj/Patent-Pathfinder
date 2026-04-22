from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class IdeaCreate(BaseModel):
    title: str
    problem_statement: str
    domain: str
    objectives: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class EvidenceItem(BaseModel):
    source_id: str
    source_type: str
    title: str
    passage: str
    score: float
    citation: str


class NoveltyAnalysis(BaseModel):
    overlap_score: float
    saturation_level: str
    recommendations: list[str]
    clusters: list[dict[str, Any]] = Field(default_factory=list)


class Feature(BaseModel):
    id: str
    name: str
    novelty_label: str


class PriorArt(BaseModel):
    publication_number: str
    title: str
    evidence: list[str]


class FeatureEvidence(BaseModel):
    feature_id: str
    feature_name: str
    overlap_label: str
    evidence: list[str]


class NoveltyMap(BaseModel):
    high_saturation: list[str] = Field(default_factory=list)
    moderate_saturation: list[str] = Field(default_factory=list)
    potential_novelty_hotspots: list[str] = Field(default_factory=list)


class IdeaResponse(BaseModel):
    idea_id: str
    title: str
    status: str
    created_at: datetime
    analysis_mode: str | None = None
    retrieval_source: str | None = None
    evidence: list[EvidenceItem] = Field(default_factory=list)
    novelty: NoveltyAnalysis | None = None
    decomposed_features: list[Feature] = Field(default_factory=list)
    top_prior_art: list[PriorArt] = Field(default_factory=list)
    feature_to_evidence_mapping: list[FeatureEvidence] = Field(default_factory=list)
    novelty_map: NoveltyMap = Field(default_factory=NoveltyMap)
    redesign_suggestions: list[str] = Field(default_factory=list)
    suggested_cpc_codes: list[str] = Field(default_factory=list)
    suggested_search_expansions: list[str] = Field(default_factory=list)


class ProjectSummary(BaseModel):
    project_id: str
    title: str
    domain: str
    status: str
    updated_at: datetime


class ReportRequest(BaseModel):
    idea_id: str
    format: str = Field(pattern='^(pdf|csv)$')


class ReportResponse(BaseModel):
    artifact_path: str
    format: str
    download_url: str | None = None
