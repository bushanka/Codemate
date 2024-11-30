import seedir as sd

from codemate.adapters.llm_api.client import AIClient
from codemate.adapters.llm_api.shemas import Message, AIResponse
from codemate.application.agents.base import Agent
from codemate.application.agents.tree_split.prompts import SYSTEM_PROMPT_TREE_SPLIT, USER_PROMPT_TREE_ANALYZE


class TreeSplitAgent(Agent):
    def __init__(self):
        self._client = AIClient(verbose=False)

    def create_report(self, *args, **kwargs) -> AIResponse:
        project_path = kwargs.get('project_path')
        if project_path is None:
            raise Exception('ProjectPath is None')

        project_tree = sd.seedir(project_path, indent=2, printout=False)

        messages = [
            Message(role="system", content=SYSTEM_PROMPT_TREE_SPLIT),
            Message(role="user", content=USER_PROMPT_TREE_ANALYZE.format_map({"project_tree": project_tree}))
        ]
        response = self._client.generate(messages)

        return response
