from langchain.memory import ConversationTokenBufferMemory
from langchain.chat_models import ChatOpenAI


llm = ChatOpenAI()

memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=10)
memory.save_context({"input": "hi"}, {"output": "whats up"})
memory.save_context({"input": "not much you"}, {"output": "not much"})

from langchain.chains import ConversationChain

conversation_with_summary = LLMChain(
    llm=llm,
    # We set a very low max_token_limit for the purposes of testing.
    memory=ConversationTokenBufferMemory(llm=OpenAI(), max_token_limit=60),
    verbose=True,
)
conversation_with_summary.predict(input="Hi, what's up?")
