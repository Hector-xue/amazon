from __future__ import annotations

from .ai_client import AIClient
from .prompts import EMAIL_SYSTEM_PROMPT
from .schemas import EmailReply


def draft_email_reply(ai: AIClient, scenario: str, buyer_message: str) -> dict:
    return ai.generate_json(
        system_prompt=EMAIL_SYSTEM_PROMPT,
        user_payload={"scenario": scenario, "buyer_message": buyer_message},
        output_model=EmailReply,
    )

