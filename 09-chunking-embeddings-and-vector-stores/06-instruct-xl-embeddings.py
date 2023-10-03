from InstructorEmbedding import INSTRUCTOR

# pip install torch
# pip install sentence_transformers

model = INSTRUCTOR("hkunlp/instructor-xl")
sentence = "3D ActionSLAM: wearable person tracking in multi-floor environments"
instruction = "Represent the Science title:"
embeddings = model.encode([[instruction, sentence]])
print(embeddings)
