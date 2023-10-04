from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceInstructEmbeddings

url_list = [
    "https://www.youtube.com/watch?v=0e3GPea1Tyg",
    "https://www.youtube.com/watch?v=zxYjTTXc-J8",
    "https://www.youtube.com/watch?v=9bqk6ZUsKyA",
    "https://www.youtube.com/watch?v=iogcY_4xGjo",
    "https://www.youtube.com/watch?v=r7zJ8srwwjk",
    "https://www.youtube.com/watch?v=GLoeAJUcz38",
    "https://www.youtube.com/watch?v=fMfipiV_17o",
    "https://www.youtube.com/watch?v=1WEAJ-DFkHE",
    "https://www.youtube.com/watch?v=yXWw0_UfSFg",
    "https://www.youtube.com/watch?v=gHzuabZUd6c",
    "https://www.youtube.com/watch?v=QxGVgXf_LNk",
]

documents = []

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=450,
    chunk_overlap=50,
)

for url in url_list:
    loader = YoutubeLoader.from_youtube_url(
        url,
        add_video_info=True,
    )
    loader = loader.load_and_split(text_splitter=text_splitter)
    documents = documents + loader

embedding_function = HuggingFaceInstructEmbeddings(
    model_name="hkunlp/instructor-base",
)

db = Chroma.from_documents(
    documents,
    embedding_function,
    persist_directory="./10-Retriver-Augmented-Generation/mr-beast-db",
)

db.persist()

docs = db.similarity_search("what was the type of car that cost $1?", k=2)
print(docs)
