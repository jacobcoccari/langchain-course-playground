from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
)
from discord_bot import DiscordClient
import langchain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

langchain.debug = True


class Controller:
    def __init__(self, openai_api_key, discord_api_key) -> None:
        self.discord_api_key = discord_api_key
        self.embedding_function = OpenAIEmbeddings()
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        self.compressor = LLMChainExtractor.from_llm(self.llm)
        self.retriver = Chroma(
            persist_directory="./langchain_documents_db/",
            embedding_function=self.embedding_function,
        ).as_retriever()

        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm, chain_type="map_reduce", retriever=self.retriver
        )

    def query(self, query):
        prompt = PromptTemplate(
            template="{query}",
            input_variables=["query"],
        )
        _input = prompt.format_prompt(query=query).to_string()
        # print(self.db_connection.similarity_search(_input)[0].page_content)
        search = self.qa({"query": _input})
        return search["result"]

    def run(self):
        discord_client = DiscordClient(self.query)
        discord_client.run(self.discord_api_key)
