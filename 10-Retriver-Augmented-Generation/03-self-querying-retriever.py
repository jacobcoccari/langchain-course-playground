from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# pip install lark

from dotenv import load_dotenv

load_dotenv()

embedding_function = HuggingFaceInstructEmbeddings(
    model_name="hkunlp/instructor-base",
)

db = Chroma(
    persist_directory="./10-Retriver-Augmented-Generation/crash-course-db",
    embedding_function=embedding_function,
)
# Take a look at the metadata
# print(db.similarity_search("who was ashoka?"))

metadata_field_info = [
    AttributeInfo(
        name="author",
        description="The author of the video transcript",
        type="string or list[string]",
    ),
    AttributeInfo(
        name="description",
        description="the description of the video",
        type="string",
    ),
    AttributeInfo(
        name="publish_date",
        description="The date that the video was originally published",
        type="datetime",
    ),
    AttributeInfo(name="source", description="The youtube URL slug.", type="string"),
    AttributeInfo(
        name="thumbnail_url",
        description="The URL for the video thumbnail.",
        type="string",
    ),
    AttributeInfo(
        name="title",
        description="the title of the video",
        type="string",
    ),
    AttributeInfo(
        name="view_count",
        description="The total number of views for the video",
        type="int",
    ),
]
model = OpenAI()
description = "Metadata and transcripts from a youtube video."
retriever = SelfQueryRetriever.from_llm(
    llm=model,
    vectorstore=db,
    document_contents=description,
    metadata_field_info=metadata_field_info,
    verbose=True,
    k=1,
)

query = "What video has the most total views?"
response = retriever.get_relevant_documents(query)
print(response)
