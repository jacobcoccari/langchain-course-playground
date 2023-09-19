from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.chains import LLMChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import PydanticOutputParser
from discord_bot import DiscordClient
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router import MultiPromptChain
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
import langchain
from langchain.schema import SystemMessage

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage


class Controller:
    def __init__(self, openai_api_key, discord_api_key) -> None:
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="You are a helpful AI assistant. Include tables, code snippets, and concise descriptions to help the user."
                ),  # The persistent system prompt
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template(
                    "{human_input}"
                ),  # Where the human input will injected
            ]
        )
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=openai_api_key,
            temperature=0.0,
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.conversation = LLMChain(
            llm=self.llm,
            prompt=prompt,
            verbose=True,
            memory=self.memory,
        )
        # langchain.debug = True
        self.discord_api_key = discord_api_key
        self.step = "start"

    def query(self, query):
        prompt = PromptTemplate(
            template="{query}",
            input_variables=["query"],
        )
        _input = prompt.format_prompt(query=query).to_string()
        return self.conversation.predict(human_input=_input)

    def run(self):
        discord_client = DiscordClient(self.query)
        discord_client.run(self.discord_api_key)
