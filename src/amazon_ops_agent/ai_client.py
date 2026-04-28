from __future__ import annotations

import json
from typing import Any, Type

from openai import OpenAI
from pydantic import BaseModel

from .config import Settings


class AIClient:
    def __init__(self, settings: Settings) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is required for AI generation tasks.")
        self.model = settings.openai_model
        self.client = OpenAI(api_key=settings.openai_api_key)

    def generate_json(
        self,
        *,
        system_prompt: str,
        user_payload: dict[str, Any],
        output_model: Type[BaseModel],
    ) -> dict[str, Any]:
        schema = output_model.model_json_schema()
        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": output_model.__name__,
                    "schema": schema,
                    "strict": True,
                }
            },
        )
        content = response.output_text
        parsed = output_model.model_validate_json(content)
        return parsed.model_dump()

