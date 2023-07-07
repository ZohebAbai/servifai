import os

from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI

load_dotenv()


class OpenAI:
    def __init__(self, llmconfigs):
        self._name = llmconfigs["model"]
        self._temp = int(llmconfigs["temperature"])
        self._max_tokens = int(llmconfigs["max_tokens"])
        self.model = self._get_openai_model()

    def _get_openai_model(self):
        if os.getenv("OPENAI_API_TYPE") == "azure":
            return AzureChatOpenAI(
                openai_api_type="azure",
                deployment_name=os.getenv("DEPLOYMENT_ID"),
                openai_api_base=os.getenv("OPENAI_API_BASE"),
                openai_api_version=os.getenv("OPENAI_API_VERSION"),
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                temperature=self._temp,
                max_tokens=self._max_tokens,
                streaming=True,
                model_kwargs={
                    "frequency_penalty": 0.3,  # TODO:to be provided from user-end
                },
            )
        return ChatOpenAI(
            temperature=self._temp,
            model_name=self._name,
            max_tokens=self._max_tokens,
            streaming=True,
            model_kwargs={
                "frequency_penalty": 0.3,  # TODO: to be provided from user-end
            },
        )
