from langchain.agents import initialize_agent
from langchain.chains.conversation.memory import ConversationBufferMemory

from servifai.toolbox import BaseToolBox


class ReactChatAgent:
    def __init__(self, task, llm, dbdir, datadir, dataconfigs, memoryconfigs):
        self.llm = llm
        self.toolbox = BaseToolBox(
            task, llm, dbdir, datadir, dataconfigs, memoryconfigs
        ).toolbox
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

    def query(self, query: str):
        agent = initialize_agent(
            self.toolbox,
            self.llm.model,
            agent="chat-conversational-react-description",
            verbose=True,
            memory=self.memory,
            max_iterations=3,
            # early_stopping_method='generate',
        )
        return agent.run(input=query)
