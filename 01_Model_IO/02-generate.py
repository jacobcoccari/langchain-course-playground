import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
import pprint as pp

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def main():
    llm = OpenAI(openai_api_key=api_key, model="gpt-3.5-turbo-instruct")
    result = llm.generate(["is this working?"]).dict()
    print(pp.pp(result))
    print(type(result))


if __name__ == "__main__":
    main()
