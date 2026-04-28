from __future__ import annotations

from .ai_client import AIClient
from .prompts import LISTING_SYSTEM_PROMPT
from .schemas import ListingPlan, ProductBrief


def optimize_listing(ai: AIClient, product: dict) -> dict:
    brief = ProductBrief.model_validate(product)
    return ai.generate_json(
        system_prompt=LISTING_SYSTEM_PROMPT,
        user_payload={"product": brief.model_dump()},
        output_model=ListingPlan,
    )

