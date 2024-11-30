from codemate.adapters.llm_api.client import AIClient
from codemate.adapters.llm_api.shemas import Message, AIResponse
from codemate.application.agents.base import Agent
from codemate.application.agents.code_analyzer.prompts import SYSTEM_PROMPT_CODE_ANALYZE, USER_PROMPT_CODE_ANALYZE


class CodeAnalyzerAgent(Agent):
    def __init__(self):
        self._client = AIClient(verbose=False)

    def create_report(self, *args, **kwargs) -> AIResponse:
        file_path = kwargs.get('file_path')
        layer_name = kwargs.get('layer_name')
        code_content = kwargs.get('code_content')
        if file_path is None:
            raise Exception('FilePath is None')
        if layer_name is None:
            raise Exception('LayerName is None')
        if code_content is None:
            raise Exception('CodeContent is None')

        params_map = {
            'file_path': file_path,
            'layer_name': layer_name,
            'code_content': code_content
        }

        messages = [
            Message(role='system', content=SYSTEM_PROMPT_CODE_ANALYZE),
            Message(role='user', content=USER_PROMPT_CODE_ANALYZE.format_map(params_map))
        ]
        response = self._client.generate(messages)

        return response
