
import numpy as np

from src.utils.embedding_utils import generate_embedding


def calculate_similarity(text1, text2):
    """Calculate cosine similarity between two text embeddings."""

    if not isinstance(text1, str) or not text1.strip():
        raise ValueError("First text must be a non-empty string.")

    if not isinstance(text2, str) or not text2.strip():
        raise ValueError("Second text must be a non-empty string.")

    vector1 = np.array(generate_embedding(text1))
    vector2 = np.array(generate_embedding(text2))

    denominator = np.linalg.norm(vector1) * np.linalg.norm(vector2)

    if denominator == 0:
        return 0.0

    similarity = np.dot(vector1, vector2) / denominator

    return float(similarity)


def compare_resume_and_job(resume_text, job_description):
    """Return a semantic similarity indicator for two text documents."""

    similarity = calculate_similarity(resume_text, job_description)

    # Convert cosine similarity from [-1, 1] to [0, 100].
    score = ((similarity + 1) / 2) * 100

    return {
        "cosine_similarity": round(similarity, 4),
        "semantic_similarity_score": round(score, 2),
    }
