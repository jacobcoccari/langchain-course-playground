from dotenv import load_dotenv

from langchain.chains import SequentialChain
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate


load_dotenv()

from langchain.chat_models import ChatOpenAI

# This is an LLMChain to write a synopsis given a title of a play and the era it is set in.
model = ChatOpenAI()
synopsis_template = """You are a playwright. Given the title of play and the era it is set in, \
                    it is your job to write a synopsis for that title. Be concise.

Title: {title}
Era: {era}
Playwright: This is a synopsis for the above play:"""
synopsis_prompt_template = ChatPromptTemplate.from_template(synopsis_template)
# input_variables=["title", "era"], template=synopsis_template

synopsis_chain = LLMChain(
    llm=model,
    prompt=synopsis_prompt_template,
    output_key="synopsis",
)

# This is an LLMChain to write a review of a play given a synopsis.
review_template = """You are a play critic from the New York Times. Given the synopsis of play, it is \
            your job to write a review for that play. Be concise.

Play Synopsis:
{synopsis}
Review from a New York Times play critic of the above play:"""
review_prompt_template = ChatPromptTemplate.from_template(review_template)
# input_variables=["synopsis"], template=template
review_chain = LLMChain(
    llm=model,
    prompt=review_prompt_template,
    output_key="review",
)

# This is the overall chain where we run these two chains in sequence.

overall_chain = SequentialChain(
    chains=[synopsis_chain, review_chain],
    input_variables=["era", "title"],
    # Here we return multiple variables
    output_variables=["synopsis", "review"],
)

# .run is not supported for SequentialChain since there is more than one output key, .generate not supportede
result = overall_chain.predict(
    [
        {"title": "Tragedy at sunset on the beach", "era": "Victorian England"},
        {"title": "Tragedy at sunset on the beach", "era": "Modern Broadway"},
    ]
)
print(result)
