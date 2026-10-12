
import re


def evaluate_answer(answer, question="", topic="", category=""):
    """
    Evaluate an interview answer using simple, transparent rules.
    This is a practice aid, not a true AI or semantic evaluation.
    """

    
    if not isinstance(answer, str):
        answer = ""

    answer = answer.strip()

    if not answer:
        return {
            "score": 0,
            "level": "No answer",
            "word_count": 0,
            "strengths": [],
            "improvements": [
                "Write an answer before requesting an evaluation.",
            ],
            "suggested_structure": [
                "Start with a clear definition or direct answer.",
                "Explain the key technical details and how they work.",
                "Give an example, application, or project experience.",
                "Conclude with the main benefit, limitation, or trade-off.",
            ],
        }


    words = re.findall(r"\b[\w+#.-]+\b", answer)
    word_count = len(words)
    sentences = [
        sentence.strip()
        for sentence in re.split(r"[.!?]+", answer)
        if sentence.strip()
    ]

    score = 0
    strengths = []
    improvements = []

    # 1. Completeness: reward answers with enough detail.
    if word_count >= 80:
        score += 30
        strengths.append("Your answer provides a reasonable amount of detail.")
    elif word_count >= 40:
        score += 22
        strengths.append("Your answer has a useful starting level of detail.")
    elif word_count >= 20:
        score += 14
        improvements.append("Add more explanation and at least one relevant example.")
    else:
        score += 5
        improvements.append("Expand your answer with a definition, explanation, and example.")

    # 2. Structure: look for multiple sentences.
    if len(sentences) >= 4:
        score += 20
        strengths.append("Your answer uses several sentences to explain the idea.")
    elif len(sentences) >= 2:
        score += 14
        strengths.append("Your answer has some explanatory structure.")
    else:
        score += 5
        improvements.append("Organize the answer into a few clear sentences.")

    # 3. Examples and applications: basic phrase matching.
    example_phrases = [
        "for example", "for instance", "such as",
        "in practice", "in a project", "we can use",
        "used to", "application"
    ]

    if any(phrase in answer.lower() for phrase in example_phrases):
        score += 25
        strengths.append("You included an example or practical application.")
    else:
        improvements.append("Include a practical example or real-world application.")

    # 4. Explanation and reasoning: look for explanatory connectors.
    reasoning_phrases = [
        "because", "therefore", "however", "which means",
        "as a result", "the reason", "in contrast",
        "this helps", "this allows"
    ]

    if any(phrase in answer.lower() for phrase in reasoning_phrases):
        score += 25
        strengths.append("You attempted to explain reasoning or relationships.")
    else:
        improvements.append("Explain why the concept works and when it is useful.")

    score = min(score, 100)

    # Limit the score for answers that are too short.
    if word_count < 20:
        score = min(score, 25)
    elif word_count < 40:
        score = min(score, 45)
    elif word_count < 80:
        score = min(score, 65)

    if score >= 80:
        level = "Strong structure"
    elif score >= 60:
        level = "Good start"
    elif score >= 40:
        level = "Needs improvement"
    else:
        level = "Needs more detail"

    if not improvements:
        improvements.append(
            "Add precise technical details and check that each claim is correct."
        )

    return {
        "score": score,
        "level": level,
        "word_count": word_count,
        "strengths": strengths,
        "improvements": improvements,
        "suggested_structure": [
            "Start with a clear definition or direct answer.",
            "Explain the key technical details and how they work.",
            "Give an example, application, or project experience.",
            "Conclude with the main benefit, limitation, or trade-off.",
        ],
    }
