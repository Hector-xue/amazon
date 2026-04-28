from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ProductBrief(BaseModel):
    asin: str | None = None
    marketplace: str = "US"
    product_name: str
    brand: str | None = None
    category: str | None = None
    target_customer: str | None = None
    features: list[str] = Field(default_factory=list)
    benefits: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    competitor_notes: str | None = None
    tone: str = "clear, compliant, benefit-focused English"


class ListingPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    bullet_points: list[str]
    product_description: str
    search_terms: list[str]
    image_selling_points: list[str]
    compliance_notes: list[str]


class EmailReply(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject: str
    reply: str
    compliance_notes: list[str]
    next_action: str


class ImageBrief(BaseModel):
    model_config = ConfigDict(extra="forbid")

    image_type: str
    objective: str
    scene: str
    key_visual_elements: list[str]
    copy_suggestion: str
    production_notes: list[str]


class ImagePlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    briefs: list[ImageBrief]
    overall_notes: list[str]


class KeywordAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    term: str
    campaign: str | None = None
    ad_group: str | None = None
    reason: str
    metrics: dict[str, Any]
    recommendation: str


class AdsAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: dict[str, Any]
    high_spend_low_conversion: list[KeywordAction]
    low_acos_winners: list[KeywordAction]
    negative_keyword_candidates: list[KeywordAction]
    budget_adjustment_candidates: list[KeywordAction]
    rows: list[dict[str, Any]]


TaskName = Literal["listing", "email", "images"]
