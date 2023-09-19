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
            model="gpt-4",
            openai_api_key=openai_api_key,
            temperature=0.0,
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.conversation = LLMChain(
            llm=self.llm,
            prompt=prompt,
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
