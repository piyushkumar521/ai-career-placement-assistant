
from sentence_transformers import SentenceTransformer

# Load the model once and reuse it.
_model = None


def get_embedding_model():
    """Load the embedding model only when first needed."""
    global _model

    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    return _model


def generate_embedding(text):
    """Convert one text string into a numerical embedding."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text must be a non-empty string.")

    model = get_embedding_model()
    embedding = model.encode(text, normalize_embeddings=True)

    return embedding.tolist()


def generate_embeddings(texts):
    """Convert multiple text strings into numerical embeddings."""
    if not texts:
        return []

    if not all(isinstance(text, str) and text.strip() for text in texts):
        raise ValueError("Every item must be a non-empty string.")

    model = get_embedding_model()
    embeddings = model.encode(texts, normalize_embeddings=True)

    return embeddings.tolist()
