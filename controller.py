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
import pickle
import time

# Our model
from langchain.chat_models import ChatOpenAI

# This retriever
from langchain.retrievers import ContextualCompressionRetriever

# This allows us to use
from langchain.retrievers.document_compressors import LLMChainExtractor


langchain.debug = True


class Controller:
    def __init__(self, openai_api_key, discord_api_key) -> None:
        self.discord_api_key = discord_api_key
        self.embedding_function = OpenAIEmbeddings()
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        self.compressor = LLMChainExtractor.from_llm(self.llm)
        self.db_connection = Chroma(
            persist_directory="./langchain_documents_db/",
            embedding_function=self.embedding_function,
        )
        self.compression_retriever = ContextualCompressionRetriever(
            base_compressor=self.compressor,
            base_retriever=self.db_connection.as_retriever(),
        )

    def query(self, query):
        prompt = PromptTemplate(
            template="{query}",
            input_variables=["query"],
        )
        _input = prompt.format_prompt(query=query).to_string()
        # print(self.db_connection.similarity_search(_input)[0].page_content)
        search = self.compression_retriever.get_relevant_documents(_input)
        return search[0].page_content

    def run(self):
        discord_client = DiscordClient(self.query)
        discord_client.run(self.discord_api_key)
