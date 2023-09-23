from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def main():
    model = ChatOpenAI(openai_api_key=api_key)
    prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
    chain = prompt | model

    # for a singular call to the langchain expression model, we use .invoke()
    result = chain.invoke({"topic": "bears"})
    print(result.content)
    print(type(result))

if __name__ == "__main__":
    main()