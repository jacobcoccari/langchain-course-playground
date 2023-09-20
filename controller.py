from discord_bot import DiscordClient
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma


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
            llm=self.llm,
            chain_type="map_reduce",
            retriever=self.retriver,
            return_source_documents=True,
        )

    def query(self, query):
        prompt = PromptTemplate(
            template="{query}",
            input_variables=["query"],
        )
        _input = prompt.format_prompt(query=query).to_string()
        search = self.qa({"query": _input})
        unique_source_documents = set(
            [
                source_document.metadata["source"]
                for source_document in search["source_documents"]
            ]
        )
        source_string = "\n"
        for source_document in unique_source_documents:
            source_string = source_string + source_document + "\n"

        full_response = search["response"] + source_string
        return full_response

    def run(self):
        discord_client = DiscordClient(self.query)
        discord_client.run(self.discord_api_key)
