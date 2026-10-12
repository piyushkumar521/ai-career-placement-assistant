
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


from src.utils.answer_evaluation_utils import detect_question_type


def test_detect_technical_question():
    question = "Explain how a random forest works."
    assert detect_question_type(question) == "Technical"


def test_detect_behavioral_question():
    question = "Tell me about a time you solved a difficult technical problem."
    assert detect_question_type(question) == "Behavioral"


def test_behavioral_answer_gets_star_structure():
    result = evaluate_answer(
        answer="During my project, my task was to improve accuracy. "
        "I analyzed the data and implemented a better feature selection method. "
        "As a result, the model performed better. I learned to validate "
        "features carefully before training.",
        question="Tell me about a time you solved a technical challenge.",
    )

    
    assert result["question_type"] == "Behavioral"

    for section in ["Situation", "Task", "Action", "Result"]:
        assert any(
            section in item
            for item in result["suggested_structure"]
        )



def test_technical_answer_gets_technical_structure():
    result = evaluate_answer(
        answer="Random forest is an ensemble learning method. "
        "It combines multiple decision trees to improve predictions. "
        "For example, it can be used for classification. "
        "This helps reduce overfitting compared with a single tree.",
        question="Explain how a random forest works.",
    )

    assert result["question_type"] == "Technical"
    assert any(
        "definition" in item.lower()
        for item in result["suggested_structure"]
    )
