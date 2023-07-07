# Import Libraries
import logging
import sys
from pathlib import Path

import yaml

from servifai.llm import BaseLLM
from servifai.planning import ReactChatAgent

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

BASE_DIR = Path(__file__).parent.parent.absolute()
LOGS_DIR = Path(BASE_DIR, "logs")
DEFAULT_CONFIG = Path(BASE_DIR, "servifai/default_config.yaml")


class ServifAI:
    def __init__(self, config_file=None):
        """Initializes a ServifAI instance with specific config for a given task

        Args:
            cfg (DictConfig): specific constants for a particular data
        """
        self.cfg = self._load_config(config_file)
        self.task = self.cfg["task"]
        self.llm = BaseLLM(self.cfg["llm"]).llm
        self.agent = ReactChatAgent(
            self.task,
            self.llm,
            Path(BASE_DIR, self.cfg["memory"]["dir"]),
            Path(BASE_DIR, self.cfg["data"]["dir"]),
            self.cfg["data"],
            self.cfg["memory"],
        )

    def _load_config(self, config_file):
        config = None
        if config_file is not None and Path(config_file).exists():
            with open(config_file, "r") as file:
                config = yaml.safe_load(file)
        else:
            logging.warning(
                "No Config file provided by user, hence switching to default!"
            )
            with open(DEFAULT_CONFIG, "r") as file:
                config = yaml.safe_load(file)
        return config

    def chat(self, question: str):
        """Responds to user query as chat conversation

        Args:
            question (str): user query

        Returns:
            str: Response
        """
        try:
            if not question:
                logging.warning("No input text provided by user")
                return "No input provided by user"
            logging.info("Generating response:")
            return self.agent.query(question)
        except Exception as e:
            logging.error(f"Error: {e}")
