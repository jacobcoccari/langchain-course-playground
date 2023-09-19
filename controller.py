from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
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
from langchain.schema import SystemMessage

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)


class Controller:
    def __init__(self, openai_api_key, discord_api_key) -> None:
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=openai_api_key,
            temperature=0.0,
        )
        # langchain.debug = True
        self.conversation = ConversationChain(llm=self.llm, memory=self.memory)
        self.discord_api_key = discord_api_key
        self.step = "start"

    # This function uses a router chain and returns a peice of structured data that tells us the next step for the user.
    def diagnose_problem(self, query):
        prompt_infos = [
            {
                "name": "book_flight",
                "description": "Used to help a user book a new flight",
            },
            {
                "name": "change_flight",
                "description": "Used to help a user change their flight",
            },
            {
                "name": "find_bag",
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
        router_chain_decision = router_chain(query)["destination"]
        if router_chain_decision == None:
            return "start"
        return router_chain_decision
        # if router_chain_decision == None:
        #     return "start"
        # else:
        #     return router_chain_decision

    def change_flight():
        pass

    def book_flight():
        pass
    
    def find_bag(self, query):
        
    # Take a user input and retrun a response
    def query(self, query):
        prompt = PromptTemplate(
            template="{query}",
            input_variables=["query"],
        )
        _input = prompt.format_prompt(query=query).to_string()
        if self.step == "start":
            problem = self.diagnose_problem(_input)
            self.step = problem
            return problem
        while self.step == "find_bag":
            return self.find_bag(_input)
            # print(self.memory)
            # self.memory.add_ai_message("is this working?")
            # print(self.memory)
            # self.memory.save_context(
            #     {
            #         "input": "You are a helpful AI assistant. Please collect the following information: \n 1) Name and 2) Booking number"
            #     }
            # )
        # else:
        #     output = self.conversation.predict(input=_input)
        #     print("--------------------------")
        #     print(self.memory)
        #     return output

    def run(self):
        discord_client = DiscordClient(self.query)
        discord_client.run(self.discord_api_key)
