
from src.utils.answer_evaluation_utils import evaluate_answer


def test_empty_answer():
    result = evaluate_answer("")
    assert result["score"] == 0
    assert result["level"] == "No answer"
    assert result["word_count"] == 0


def test_none_answer():
    result = evaluate_answer(None)
    assert result["score"] == 0
    assert result["level"] == "No answer"


def test_short_answer():
    result = evaluate_answer("Python is useful.")
    assert result["word_count"] > 0
    assert 0 <= result["score"] <= 100
    assert result["improvements"]


def test_detailed_answer():
    answer = (
        "Python is a high-level programming language. "
        "It is widely used because it has a simple syntax. "
        "For example, I used Python in a project to automate data processing. "
        "This helps reduce repetitive work and improve efficiency."
    )
    result = evaluate_answer(answer)
    assert result["word_count"] > 0
    assert result["score"] >= 0
    assert result["strengths"]
    assert result["suggested_structure"]


def test_short_answer_score_is_capped():
    answer = (
        "Python is useful because it is simple. "
        "For example, it helps automate tasks."
    )
    result = evaluate_answer(answer)

    assert result["word_count"] < 40
    assert result["score"] <= 45
