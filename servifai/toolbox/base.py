from .default import DefaultTools
from .knowledge_base import KnowledgeBase


class BaseToolBox:
    """Base class for ServifAI Toolbox"""

    def __init__(self, task, llm, dbdir, datadir, dataconfigs, memoryconfigs):
        self.task = task
        self.llm = llm
        self.dbdir = dbdir
        self.datadir = datadir
        self.about = dataconfigs["about"]
        self.memoryconfigs = memoryconfigs
        self.toolbox = self._get_toolbox()

    def _get_toolbox(self):
        default_tool = DefaultTools(self.llm.model)
        if self.task == "qna_local_docs":
            knowledge_base = KnowledgeBase(
                self.dbdir,
                self.datadir,
                self.about,
                self.memoryconfigs,
                self.llm,
            )
            return knowledge_base.as_tool()
        return default_tool.as_tool()
