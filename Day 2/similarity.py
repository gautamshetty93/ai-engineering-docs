"""
About:
This program demonstrates semantic similarity using text embeddings.
It converts sentences into vectors using a pre-trained SentenceTransformer
model and compares them using cosine similarity.

Prerequisites:
- Python 3.x
- Install dependency:
    pip install sentence-transformers

How to run:
    python similarity.py

Expected result:
Semantically similar sentences should have a higher cosine similarity
score than unrelated sentences.
"""

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# Load a pre-trained embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Sentences to compare
sentences = [
    "I love programming in Java",
    "Java is my favorite programming language",
    "I enjoy cooking Italian food"
]

# Convert sentences into embeddings (vectors)
embeddings = model.encode(sentences)

# Compare every pair of sentences
for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):

        similarity = cos_sim(
            embeddings[i],
            embeddings[j]
        ).item()

        print(f"\nSentence 1: {sentences[i]}")
        print(f"Sentence 2: {sentences[j]}")
        print(f"Cosine similarity: {similarity:.4f}")