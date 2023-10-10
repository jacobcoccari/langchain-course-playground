prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="You are a chatbot speaking in pirate english."
        ),  # The persistent system prompt
        MessagesPlaceholder(
            variable_name="chat_history"
        ),  # Where the memory will be stored.
        HumanMessagePromptTemplate.from_template(
            "{human_input}"
        ),  # Where the human input will injected
    ]
)
