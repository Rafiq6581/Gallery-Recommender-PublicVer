from __future__ import annotations
import json
import re
from loguru import logger

from gallery_recommender.domain.inference import Inference
from gallery_recommender.settings import settings
from typing import Optional, Dict


class InferenceExecutor:
    def __init__(
        self,
        llm: Inference,
        query: dict,
        filters: Optional[Dict[str, str]],
        context: str | None = None,
        prompt_template: str | None = None,
    ) -> None:
        self.llm = llm
        self.query = query
        self.filters = filters
        self.context = (context or "").strip()
        # A clearer few‐shot template, with bullet‐points
        self.prompt_template = prompt_template or """
        You are an AI language model assistant. Your task is to generate a concise and engaging report based on the user's input and the provided gallery and exhibition information.

        Use the following user inputs to tailor your response:
        * Art Knowledge Level: {level}
        * Reason for Gallery Visit: {reason}
        * Time Available: {time_available}
        * Current Mood: {mood}
        """
        
    def sanitize_llm_json(raw: str) -> str:
        # Replace curly quotes with straight quotes
        raw = raw.replace('“', '"').replace('”', '"')
        # Optionally replace any triple quotes if they appear
        raw = raw.replace("'''", '"').replace('"""', '"')
        # Remove weird invisible unicode characters
        raw = re.sub(r'[\u200b-\u200f\u202a-\u202e]', '', raw)
        return raw

    def execute(self) -> dict:
        # 1) render the prompt
        prompt = self.prompt_template.format(query=self.query, filters=self.filters, context=self.context)
        logger.info(f"Prompt: {prompt!r}")
        # 2) set payload
        self.llm.set_payload(
            new_query=prompt,
            parameters={
                "temperature": settings.OPENAI_TEMPERATURE,
                "max_tokens": settings.OPENAI_MAX_TOKENS,
                "top_p": settings.OPENAI_TOP_P,
            },
        )

        # 3) invoke the model
        result = self.llm.inference()

        # 4) extract raw text from whatever shape you got back
        if isinstance(result, dict) and "choices" in result:
            raw = result["choices"][0]["message"]["content"]
            logger.info(f"LLM Output: {raw!r}")
            
        elif isinstance(result, list) and result and "generated_text" in result[0]:
            raw = result[0]["generated_text"]
        else:
            raise RuntimeError(f"Unrecognized LLM response shape: {result!r}")

        # 5) parse the JSON that the model produced
        try:
            payload = json.loads(raw)
            # report = payload["report"]
            # score = float(payload["score"])
        except Exception as e:
            raise RuntimeError(f"Failed to parse JSON from model: {raw!r}") from e

        return payload
        

    # async def execute(self):
    #         # 1) render the prompt
    #         prompt = self.prompt_template.format(query=self.query, context=self.context)

    #         # 2) set payload
    #         self.llm.set_payload(
    #             new_query=prompt,
    #             parameters={
    #                 "temperature": settings.OPENAI_TEMPERATURE,
    #                 "max_tokens": settings.OPENAI_MAX_TOKENS,
    #                 "top_p": settings.OPENAI_TOP_P,
    #             },
    #         )

    #         # 3) invoke the model (async generator)
    #         # 4) stream outputs
    #         async for result in self.llm.inference():
    #             # result is assumed to be a dict like {"generated_text": ..., "confidence": ...}
    #             # Try to parse report/score if the generated_text looks like a JSON
    #             generated_text = result.get("generated_text")
    #             if not generated_text:
    #                 continue

    #             # Try to parse if the JSON output appears to be complete
    #             try:
    #                 payload = json.loads(generated_text)
    #                 report = payload["report"]
    #                 # score = float(payload["score"])
    #                 yield {"report": report}
    #             except Exception:
    #                 # If not yet complete, just yield partial for streaming frontend
    #                 yield {"partial": generated_text}