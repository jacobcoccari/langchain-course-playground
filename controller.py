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


class Controller:
    def __init__(self, openai_api_key, discord_api_key) -> None:
        memory = ConversationBufferMemory()
        self.chat = ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=openai_api_key,
            temperature=0.0,
        )
        memory.save_context(
            {"system": "You are a helpful AI assistant"}, {"output": ""}
        )
        self.conversation = ConversationChain(llm=self.chat, memory=memory)
        self.discord_api_key = discord_api_key
        self.step = "start"

    def diagnose_problem(self, query):
        book_flight_template = """You are beehivebot, a helpful AI assistant. The user wants to book a flight.
        Please gather the following information from the user in a friendly, conversational tone:
        1) name
        2) booking number 
        Here is the user's first message:
        {input}
        """
        change_flight_template = """You are beehivebot, a helpful AI assistant. The user wants to change a flight.
        Please gather the following information from the user in a friendly, conversational tone:
        1) name
        2) booking number 
        Here is the user's first message:
        {input}
        """
        find_bag_template = """You are beehivebot, a helpful AI assistant. The user wants to find their lost bag.
        Please gather the following information from the user in a friendly, conversational tone:
        1) name
        2) bag number 
        Here is the user's first message:
        {input}
        """
        prompt_infos = [
            {
                "name": "book flight",
                "description": "User wants to book a new flight",
                "prompt_template": book_flight_template,
            },
            {
                "name": "change flight",
                "description": "User wants to change a flight",
                "prompt_template": change_flight_template,
            },
            {
                "name": "find bag",
                "description": "User wants to find a lost bag",
                "prompt_template": find_bag_template,
            },
        ]
        destination_chains = {}
        for p_info in prompt_infos:
            name = p_info["name"]
            prompt_template = p_info["prompt_template"]
            prompt = PromptTemplate(template=prompt_template, input_variables=["input"])
            chain = LLMChain(llm=self.chat, prompt=prompt)
            destination_chains[name] = chain
        default_chain = ConversationChain(llm=self.chat, output_key="text")
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
        router_chain = LLMRouterChain.from_llm(self.chat, router_prompt)
        chain = MultiPromptChain(
            router_chain=router_chain,
            destination_chains=destination_chains,
            default_chain=default_chain,
            verbose=True,
        )
        return chain.run(query)

    def change_flight():
        pass

    def book_flight():
        pass

    def find_bag():
        pass
        # Take a user input and retrun a response

    def query(self, query):
        if self.step == "start":
            self.diagnose_problem(query)
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
