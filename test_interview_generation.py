
from src.utils.interview_utils import generate_interview_questions


def generate_questions(skill, difficulty):
    return generate_interview_questions(
        target_role="AI/ML Engineer",
        resume_skills=[skill],
        required_skills=[],
        missing_skills=[],
        categories=["Fundamentals", "Practical", "Scenario", "Role-specific"],
        num_questions=10,
        difficulty=difficulty,
    )


def test_beginner_questions_include_difficulty():
    questions = generate_questions("python", "Beginner")

    assert questions
    assert all(q["difficulty"] == "Beginner" for q in questions)


def test_intermediate_questions_include_difficulty():
    questions = generate_questions("python", "Intermediate")

    assert questions
    assert all(q["difficulty"] == "Intermediate" for q in questions)


def test_advanced_questions_include_difficulty():
    questions = generate_questions("python", "Advanced")

    assert questions
    assert all(q["difficulty"] == "Advanced" for q in questions)


def test_beginner_and_advanced_have_different_question_banks():
    beginner = generate_questions("python", "Beginner")
    advanced = generate_questions("python", "Advanced")

    beginner_text = {q["question"] for q in beginner}
    advanced_text = {q["question"] for q in advanced}

    assert beginner_text != advanced_text


def test_question_count_is_within_requested_limit():
    questions = generate_questions("python", "Beginner")

    assert 1 <= len(questions) <= 10


def test_invalid_difficulty_defaults_to_intermediate():
    questions = generate_interview_questions(
        target_role="AI/ML Engineer",
        resume_skills=["python"],
        required_skills=[],
        missing_skills=[],
        categories=["Fundamentals", "Practical", "Scenario", "Role-specific"],
        num_questions=10,
        difficulty="Expert",
    )

    assert questions
    assert all(q["difficulty"] == "Intermediate" for q in questions)

def test_none_question_count_is_handled_safely():
    questions = generate_interview_questions(
        target_role="AI/ML Engineer",
        resume_skills=["python"],
        required_skills=[],
        missing_skills=[],
        categories=["Fundamentals", "Practical", "Scenario", "Role-specific"],
        num_questions=None,
        difficulty="Intermediate",
    )

    assert questions


def test_non_numeric_question_count_is_handled_safely():
    questions = generate_interview_questions(
        target_role="AI/ML Engineer",
        resume_skills=["python"],
        required_skills=[],
        missing_skills=[],
        categories=["Fundamentals", "Practical", "Scenario", "Role-specific"],
        num_questions="abc",
        difficulty="Intermediate",
    )

    assert questions

def test_zero_question_count_returns_at_least_one_question():
    questions = generate_interview_questions(
        target_role="AI/ML Engineer",
        resume_skills=["python"],
        required_skills=[],
        missing_skills=[],
        categories=["Fundamentals", "Practical", "Scenario", "Role-specific"],
        num_questions=0,
        difficulty="Intermediate",
    )

    assert questions

def test_negative_question_count_returns_at_least_one_question():
    questions = generate_interview_questions(
        target_role="AI/ML Engineer",
        resume_skills=["python"],
        required_skills=[],
        missing_skills=[],
        categories=["Fundamentals", "Practical", "Scenario", "Role-specific"],
        num_questions=-5,
        difficulty="Intermediate",
    )
    assert questions
def test_generated_questions_have_required_fields():
    questions = generate_questions("python", "Intermediate")

    assert questions
    required_fields = {"question", "topic", "category", "difficulty"}

    for question in questions:
        assert required_fields.issubset(question.keys())
        assert question["question"]
        assert question["topic"]
        assert question["category"]
        assert question["difficulty"]

def test_generated_questions_are_unique():
    questions = generate_questions("python", "Intermediate")

    question_texts = [q["question"] for q in questions]

    assert len(question_texts) == len(set(question_texts))