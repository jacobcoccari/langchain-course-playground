from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from InstructorEmbedding import INSTRUCTOR
from langchain.vectorstores import Chroma

loader = TextLoader(
    "./09-chunking-embeddings-and-vector-stores/jfk-inaguration-speech.txt"
)
speech = loader.load()[0].page_content

text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=500,
    chunk_overlap=50,
)

metadatas = [{"title": "JFK Inauguration Speech", "author": "John F. Kennedy"}]

texts_with_metadata = text_splitter.create_documents([speech], metadatas=metadatas)

embedding_function = INSTRUCTOR("hkunlp/instructor-base")

db = Chroma.from_documents(docs, embedding_function)
