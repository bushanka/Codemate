from codemate.adapters.llm_api.client import AIClient
from codemate.adapters.llm_api.shemas import Message, AIResponse
from codemate.application.agents.base import Agent
from codemate.application.agents.code_optimizer import SYSTEM_PROMPT_CODE_OPTIMIZE, USER_PROMPT_CODE_OPTIMIZE


class CodeOptimizerAgent(Agent):
    def __init__(self):
        self._client = AIClient(verbose=False)

    def create_report(self, *args, **kwargs) -> AIResponse:
        file_path = kwargs.get('file_path')
        code_content = kwargs.get('code_content')

        if file_path is None:
            raise Exception('FilePath is None')
        if code_content is None:
            raise Exception('CodeContent is None')

        params_map = {
            'file_path': file_path,
            'code_content': code_content
        }

        messages = [
            Message(role='system', content=SYSTEM_PROMPT_CODE_OPTIMIZE),
            Message(role='user', content=USER_PROMPT_CODE_OPTIMIZE.format_map(params_map))
        ]
        response = self._client.generate(messages)

        return response
