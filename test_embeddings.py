
from src.utils.embedding_utils import (
    generate_embedding,
    generate_embeddings,
)


def main():
    print("Testing single text embedding...")

    text = "Python is used for machine learning."
    vector = generate_embedding(text)

    print("Vector dimensions:", len(vector))
    print("First 5 values:", vector[:5])

    assert len(vector) == 384, "Expected a 384-dimensional vector."
    assert all(isinstance(value, float) for value in vector)

    print("\nTesting multiple text embeddings...")

    texts = [
        "Python is used for machine learning.",
        "Verilog is used for digital hardware design.",
    ]

    vectors = generate_embeddings(texts)

    print("Number of vectors:", len(vectors))
    print("Dimensions of each vector:", [len(v) for v in vectors])

    assert len(vectors) == 2
    assert all(len(v) == 384 for v in vectors)

    print("\nAll embedding tests passed!")


if __name__ == "__main__":
    main()
