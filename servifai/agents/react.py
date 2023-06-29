from langchain.chains.conversation.memory import ConversationBufferMemory
from llama_index.langchain_helpers.agents import create_llama_chat_agent


class ReactChatAgent:
    def __init__(self, task, knowledge_base, llm):
        self.task = task
        self.knowledge_base = knowledge_base
        self.llm = llm
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def chat(self, query:str):
        if self.task == 'qa_knowledge_base':
            kb_tool = self.knowledge_base.as_tool()
        agent = create_llama_chat_agent(
            kb_tool,
            self.llm.model,
            verbose=True,
            memory=self.memory,
        )
        return agent.run(input=query)
