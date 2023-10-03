from langchain.embeddings import HuggingFaceInstructEmbeddings

embeddings = HuggingFaceInstructEmbeddings(
    model_name="hkunlp/instructor-base",
    query_instruction="Represent the query for retrieval: ",
)

text = "This is a test document."

query_result = embeddings.embed_query(text)
print(query_result)
print(len(query_result))
