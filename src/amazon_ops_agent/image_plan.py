from __future__ import annotations

from .ai_client import AIClient
from .prompts import IMAGE_SYSTEM_PROMPT
from .schemas import ImagePlan, ProductBrief


def generate_image_plan(ai: AIClient, product: dict) -> dict:
    brief = ProductBrief.model_validate(product)
    return ai.generate_json(
        system_prompt=IMAGE_SYSTEM_PROMPT,
        user_payload={"product": brief.model_dump()},
        output_model=ImagePlan,
    )

