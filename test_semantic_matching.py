
from src.utils.semantic_matching_utils import (
    calculate_similarity,
    compare_resume_and_job,
)


def main():
    resume_text = (
        "I developed machine learning models using Python "
        "and evaluated their predictive performance."
    )

    similar_job_text = (
        "The candidate should build predictive models, "
        "use Python, and evaluate machine learning performance."
    )

    different_job_text = (
        "The candidate should design digital circuits "
        "using Verilog and understand RTL hardware design."
    )

    print("Testing semantic similarity...")

    similar_score = calculate_similarity(
        resume_text, similar_job_text
    )
    different_score = calculate_similarity(
        resume_text, different_job_text
    )

    print("Similar text cosine similarity:", round(similar_score, 4))
    print("Different text cosine similarity:", round(different_score, 4))

    result = compare_resume_and_job(
        resume_text, similar_job_text
    )

    print("\nResume-job comparison result:")
    print(result)

    assert -1.0 <= similar_score <= 1.0
    assert -1.0 <= different_score <= 1.0
    assert "semantic_similarity_score" in result

    print("\nAll semantic matching tests passed!")


if __name__ == "__main__":
    main()
