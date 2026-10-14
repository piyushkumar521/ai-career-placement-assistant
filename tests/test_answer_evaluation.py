
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


from src.utils.answer_evaluation_utils import (
    get_topic_guidance,
    evaluate_answer,
)


def test_python_topic_guidance():
    result = get_topic_guidance(
        question="What is a Python list?"
    )
    assert result["topic_name"] == "Python"
    assert len(result["guidance"]) == 3


def test_sql_topic_guidance():
    result = get_topic_guidance(
        question="Explain SQL joins."
    )
    assert result["topic_name"] == "SQL"
    assert len(result["guidance"]) == 3


def test_machine_learning_topic_guidance():
    result = get_topic_guidance(
        question="What is overfitting?"
    )
    assert result["topic_name"] == "Machine Learning"
    assert len(result["guidance"]) == 3


def test_deep_learning_topic_guidance():
    result = get_topic_guidance(
        question="Explain a neural network."
    )
    assert result["topic_name"] == "Deep Learning"
    assert len(result["guidance"]) == 3


def test_general_topic_guidance():
    result = get_topic_guidance(
        question="Tell me about your interests."
    )
    assert result["topic_name"] == "General"
    assert len(result["guidance"]) == 3


def test_evaluation_includes_topic_name():
    result = evaluate_answer(
        answer="Overfitting occurs when a model learns training data too closely.",
        question="What is overfitting?",
        topic="Machine Learning",
    )
    assert result["topic_name"] == "Machine Learning"


def test_empty_answer_includes_topic_name():
    result = evaluate_answer(
        answer="",
        question="Explain SQL joins.",
        topic="SQL",
    )
    assert result["topic_name"] == "SQL"


def test_behavioral_question_keeps_star_structure():
    result = evaluate_answer(
        answer="I worked on a college project and solved a difficult problem.",
        question="Tell me about a time you solved a problem.",
    )
    assert result["question_type"] == "Behavioral"
    assert any(
        item.startswith("Situation:")
        for item in result["suggested_structure"]
    )


def test_random_forest_missing_concepts_detected():
    result = evaluate_answer(
        answer="A random forest combines models to make predictions.",
        question="Explain how a random forest works.",
        topic="Machine Learning",
    )

    assert "decision tree" in result["missing_concepts"]
    assert "ensemble" in result["missing_concepts"]
    assert "overfitting" in result["missing_concepts"]


def test_missing_concepts_are_included_in_feedback():
    result = evaluate_answer(
        answer="A random forest makes predictions using multiple models.",
        question="Explain how a random forest works.",
        topic="Machine Learning",
    )

    feedback = " ".join(result["improvements"])

    assert "Consider covering these concepts" in feedback


def test_empty_answer_returns_missing_concepts():
    result = evaluate_answer(
        answer="",
        question="Explain SQL joins.",
        topic="SQL",
    )

    assert "missing_concepts" in result
    assert isinstance(result["missing_concepts"], list)
    
    

def test_detect_behavioral_question_about_teamwork():
    question = "How did you handle a disagreement with a teammate?"
    assert detect_question_type(question) == "Behavioral"


def test_detect_behavioral_question_about_failure():
    question = "Describe a failure and what you learned from it."
    assert detect_question_type(question) == "Behavioral"


def test_detect_behavioral_question_about_leadership():
    question = "Give me an example of your leadership skills."
    assert detect_question_type(question) == "Behavioral"

