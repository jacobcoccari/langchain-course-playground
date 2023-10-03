# pip install torch
# pip install sentence_transformers
# If you need to encode a shit ton of documents, it might be economically wise to use an embedding model locally.

from InstructorEmbedding import INSTRUCTOR

model = INSTRUCTOR("hkunlp/instructor-base")  # downloading a pre-trained model.
sentence = "3D ActionSLAM: wearable person tracking in multi-floor environments"
instruction = "Represent the Science title:"
embeddings = model.encode([sentence, instruction])
print(embeddings)
print(len(embeddings))
print(len(embeddings[0]))
