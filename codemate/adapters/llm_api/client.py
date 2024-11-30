import pprint
from typing import Union, List, Dict

import requests

from codemate.adapters.llm_api.shemas import Message, AIResponse
from settings import settings


class AIClient:
    def __init__(self, verbose: bool = False):
        """Initialize the AI Client."""
        self.verbose = verbose

        self.api_key = settings.api_key
        self.base_url = settings.base_url.rstrip('/')
        self.headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json',
        }

        self.model_name = settings.llm_model_name
        self.max_tokens = settings.max_tokens
        self.temperature = settings.temperature

    def generate(self, messages: Union[List[Message], List[Dict[str, str]]], ) -> AIResponse:
        """Generate a response from the AI model.

        Args:
            messages (List[Message] or List[Dict]): List of messages for the conversation

        Returns:
            AIResponse: The parsed API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
            pydantic.ValidationError: If the response doesn't match the expected schema
        """
        # Convert Message objects to dictionaries if necessary
        formatted_messages = [
            msg if isinstance(msg, dict) else msg.model_dump()
            for msg in messages
        ]

        json_data = {
            'model': self.model_name,
            'messages': formatted_messages,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
        }
        if self.verbose:
            pprint.pprint(formatted_messages)

        response = requests.post(
            f"{self.base_url}/v1/completions",
            headers=self.headers,
            json=json_data
        )
        response.raise_for_status()

        # Parse the response into our Pydantic model
        return AIResponse.model_validate(response.json())
