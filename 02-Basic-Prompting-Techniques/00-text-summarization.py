import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

from langchain.prompts import ChatPromptTemplate

load_dotenv()


def main():
    chat = ChatOpenAI()

    review = f"""I had high hopes for this reasonably priced 10 inch Fire HD Kindle tablet, but I have had nothing but trouble trying to sync my Google apps and Facebook. Can't sign in to my Google account where all my photos are and even locked out of Facebook. Tried 10 times to photo my ID to get into my locked Facebook account. So no matter how nice the screen quality or battery life I will be wiping it clean and sending it back or giving it away. Probably will buy a Google tablet and just make it easy on myself. Planned on taking this tablet with me when I travel, but I will have to find something else. 

    UPDATE- I received a call from Customer Service soon after I posted my review. The rep was able to talk me through a way to access my photos and Facebook. I will keep my tablet for the time being, but I would still not recommend it to people who really want to interface their Google account. Customer Service Rep Christian was great though!"""

    prompt = prompt = f"""Please concisely summarize the following customer review:

    ```{review}```

    """

    chat_prompt = ChatPromptTemplate.from_template(prompt)
    request = chat_prompt.format_prompt(review=review).to_messages()
    result = chat(request)
    print(result)


if __name__ == "__main__":
    main()
