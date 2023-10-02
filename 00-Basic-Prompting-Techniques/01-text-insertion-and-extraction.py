import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

from langchain.prompts import ChatPromptTemplate

load_dotenv()


def main():
    chat = ChatOpenAI()

    prompt = "The [insert] refers to rule by the father."
    result = chat([prompt])
    print(result)


if __name__ == "__main__":
    main()
