from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from discord_bot import DiscordClient
from langchain.schema import SystemMessage
import langchain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma


langchain.debug = True


class Controller:
    def __init__(self, openai_api_key, discord_api_key) -> None:
        self.llm = ChatOpenAI(
            model="gpt-4",
            openai_api_key=openai_api_key,
            temperature=0.0,
        )
        self.memory = ConversationBufferMemory(return_messages=True)
        self.conversation = LLMChain(
            llm=self.llm,
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
