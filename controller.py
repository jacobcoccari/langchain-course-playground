from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import PydanticOutputParser
from models import Name, BookingNumber
from discord_bot import DiscordClient
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router import MultiPromptChain
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
import langchain


class Controller:
    def __init__(self, openai_api_key, discord_api_key) -> None:
        memory = ConversationBufferMemory()
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=openai_api_key,
            temperature=0.0,
        )
        langchain.debug = True
        self.conversation = ConversationChain(llm=self.llm, memory=memory)
        self.discord_api_key = discord_api_key
        self.step = "start"

    # This function uses a router chain and returns a peice of structured data that tells us the next step for the user.
    def diagnose_problem(self, query):
        prompt_infos = [
            {
                "name": "book_flight",
                "description": "Used to help a user book a new flight or flights",
            },
            {
                "name": "lost_bag",
                "description": "Used to help a user find their lost bag",
            },
        ]
        destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
        destinations_str = "\n".join(destinations)
        router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
            destinations=destinations_str
        )
        router_prompt = PromptTemplate(
            template=router_template,
            input_variables=["input"],
            output_parser=RouterOutputParser(),
        )
        router_chain = LLMRouterChain.from_llm(self.llm, router_prompt)
        print(router_chain)
        return router_chain(query)

    def change_flight():
        pass

    def book_flight():
        pass

    def find_bag():
        pass
        # Take a user input and retrun a response

    def query(self, query):
        print("-------------------")
        prompt = PromptTemplate(
            template="{query}",
            input_variables=["query"],
        )
        _input = prompt.format_prompt(query=query).to_string()
        if self.step == "start":
            self.diagnose_problem(_input)
        output = self.conversation.predict(input=_input)

        return output

    def run(self):
        discord_client = DiscordClient(self.query)
        discord_client.run(self.discord_api_key)
