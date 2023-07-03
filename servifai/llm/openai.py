import os

from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI

load_dotenv()


class OpenAILLM:
    def __init__(self, llm, text):
        self._temp = int(llm["temperature"])
        self._name = llm["model_name"]
        self._oai_type = llm["org"]
        self._max_tokens = int(text["max_input_size"])
        self.model = self._get_openai_model()

    def _get_openai_model(self):
        if "azure" in self._oai_type:
            return AzureChatOpenAI(
                temperature=self._temp,
                model_name=self._name,
                max_tokens=self._max_tokens,
                streaming=True,
            )
        return ChatOpenAI(
            temperature=self._temp,
            model_name=self._name,
            max_tokens=self._max_tokens,
            streaming=True,
        )
