from loguru import logger
import requests
from gallery_recommender.domain.inference import Inference
from gallery_recommender.settings import settings



class ChatGPTInference(Inference):
    def __init__(self, query: str, model_id: str, api_key: str):
        self.query = query
        self.model_id = model_id
        self.api_key = api_key
        # initialize payload right away
        self.payload = self._default_payload()

    def _default_payload(self) -> dict:
        return {
            "model": self.model_id,
            "messages": [{"role": "user", "content": self.query}],
            "temperature": settings.OPENAI_TEMPERATURE,
            "max_tokens": settings.OPENAI_MAX_TOKENS,
            "top_p": settings.OPENAI_TOP_P,
        }

    def set_payload(self, 
                    new_query: str | None = None,
                    parameters: dict | None = None) -> None:
        """
        Optionally override the query or inject additional OpenAI parameters.
        """
        if new_query:
            # replace the user message
            self.payload["messages"] = [{"role": "user", "content": new_query}]
        if parameters:
            # merge any extra parameters in
            self.payload.update(parameters)

        logger.info(f"Payload: {self.payload}")

    def inference(self) -> dict:
        """
        Send the HTTP POST to OpenAI and return the JSON response.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            logger.info("Sending inference request to ChatGPT API")
            resp = requests.post(
                settings.OPENAI_API_URL,
                headers=headers,
                json=self.payload,
                timeout=30,
            )
            resp.raise_for_status()
            logger.info("Received response from ChatGPT API")
            return resp.json()
        except requests.RequestException as e:
            logger.error(f"OpenAI API request failed: {e}")
            raise

