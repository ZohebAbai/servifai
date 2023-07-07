from .openai import OpenAI


class BaseLLM:
    """Base class for ServifAI LLMs"""

    def __init__(self, llmconfigs):
        self.llmconfigs = llmconfigs
        self.llm = self._get_llm()

    def _get_llm(self):
        if "openai" not in self.llmconfigs["org"]:
            return None  # TODO:Check which opensource llm works good with agents
        return OpenAI(self.llmconfigs)
