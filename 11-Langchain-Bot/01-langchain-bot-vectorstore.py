from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
import pickle
import os
from dotenv import load_dotenv
import time

load_dotenv()

embedding_function = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
character_text_splitter = CharacterTextSplitter(
    separator=" ",
    chunk_size=800,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)


def read_documentation():
    new_memory_load = pickle.loads(
        open("./11-Langchain-Bot/langchain_documents.pkl", "rb").read()
    )
    docs = character_text_splitter.split_documents(new_memory_load)
    db = Chroma.from_documents(
        docs[0:2], embedding_function, persist_directory="./langchain_documents_db/"
    )
    for doc in docs:
        db.add_documents([doc])
        print("+")
        time.sleep(0.01)
        db.persist()

def read_source_code():
    

def main():
    read_documentation()
    read_source_code()


if __name__ == "__main__":
    main()
