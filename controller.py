from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import PydanticOutputParser
from models import Name, BookingNumber


memory = ConversationBufferMemory()
chat = ChatOpenAI(model="gpt-3.5-turbo")
memory.save_context({"system": "You are a helpful AI assistant"}, {"output": ""})
conversation = ConversationChain(llm=chat, memory=memory)
documents = [Name, BookingNumber]
counter = 0


def query(payload):
    return output_parser(payload)


# this function could create an agent that uses a custom tool to interact with the user every time. Make sure to add it to memory, too.
def create_agent():
    pass


def output_parser(payload):
    global counter
    print(counter)
    object = documents[counter]
    query = payload["inputs"]["text"]
    parser = PydanticOutputParser(pydantic_object=object)
    prompt = PromptTemplate(
        template="Please extract the following information from the user response.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    _input = prompt.format_prompt(query=query)
    output = conversation.predict(input=_input.to_string())
    name = parser.parse(output)
    counter += 1
    print
    return name
