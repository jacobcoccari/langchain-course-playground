from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import PydanticOutputParser
from models import Name, BookingNumber
from discord_bot import DiscordClient


class Controller:
    def __init__(self, openai_api_key, discord_api_key) -> None:
        memory = ConversationBufferMemory()
        chat = ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=openai_api_key,
            temperature=0.0,
        )
        memory.save_context(
            {"system": "You are a helpful AI assistant"}, {"output": ""}
        )
        self.conversation = ConversationChain(llm=chat, memory=memory)
        self.discord_api_key = discord_api_key

    def diagnose_problem():
        pass

    def change_flight():
        pass

    def book_flight():
        pass

    def find_bag():
        pass
        # Take a user input and retrun a response

    def query(self, query):
        prompt = PromptTemplate(
            template="{query}",
            input_variables=["query"],
        )
        _input = prompt.format_prompt(query=query)
        output = self.conversation.predict(input=_input.to_string())
        return output

    def run(self):
        discord_client = DiscordClient(self.query)
        discord_client.run(self.discord_api_key)
