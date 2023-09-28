from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import langchain

langchain.debug = True

load_dotenv()

template = """You are a chatbot having a conversation with a human.

{chat_history}
Human: {human_input}
Chatbot:"""

prompt = ChatPromptTemplate.from_template(template)

memory = ConversationBufferMemory(memory_key="chat_history")

llm = ChatOpenAI()
conversation_chain = ConversationChain(llm=llm, memory=ConversationBufferMemory())

conversation_chain.predict(input="My name is Jacob")
conversation_chain.predict(input="What is my name?")
