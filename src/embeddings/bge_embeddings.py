from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-base-en-v1.5"


class BGEEmbedder:
    """Generate embeddings using a local BGE model."""

    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:
        """Generate a single embedding."""
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()