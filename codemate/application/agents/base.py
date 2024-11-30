from typing import Protocol

from codemate.adapters.llm_api.shemas import AIResponse


class Agent(Protocol):
    def create_report(self, *args, **kwargs) -> AIResponse:
        """Generates report"""