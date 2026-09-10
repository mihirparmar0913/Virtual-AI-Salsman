from src.embeddings.bge_embeddings import BGEEmbedder


embedder = BGEEmbedder()

text = "Laptop for programming with good performance"

embedding = embedder.embed(text)

print("Embedding dimension:", len(embedding))
print("First 10 values:", embedding[:10])