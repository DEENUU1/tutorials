import os

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder
import tools
from history import CustomSQLChatMessageHistory
import langchain

load_dotenv()


langchain.debug = False


class Agent:
    __prompt = "You are an AI assistant which helps me in every day tasks. " \
        "You always need to tell the truth, if you don't know the answer you can use tools. " \
        "You follow the instructions you receive from the user as best as you can. " \
        "Feel free to use any tools available to look up. " \


    @staticmethod
    def _get_chat_openai(model: str) -> ChatOpenAI:
        return ChatOpenAI(
            temperature=0,
            model=model,
            openai_api_key=os.getenv("OPENAI_APIKEY")
        )

    @staticmethod
    def _setup_memory(session_id: str) -> ConversationBufferMemory:
        chat_message_history = CustomSQLChatMessageHistory(session_id=session_id)
        memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=True,
            chat_memory=chat_message_history,
        )

        return memory

    @staticmethod
    def _get_tools():
        return [
            tools.NotionCreateNoteTool(),
        ]

    def setup_agent(self, session_id: str, model: str) -> AgentExecutor:
        _llm = self._get_chat_openai(model=model)
        _memory = self._setup_memory(session_id=session_id)
        _tools = self._get_tools()

        prompt_agent = OpenAIFunctionsAgent.create_prompt(
            system_message=SystemMessage(content=self.__prompt),
            extra_prompt_messages=[MessagesPlaceholder(variable_name="history")]
        )

        agent = OpenAIFunctionsAgent(llm=_llm, prompt=prompt_agent, tools=_tools)
        return AgentExecutor(
            agent=agent,
            tools=_tools,
            memory=_memory,
            verbose=True,
            handle_parsing_errors=True
        )
