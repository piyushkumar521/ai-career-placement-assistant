
import re


def detect_question_type(question="", topic="", category=""):
    """Classify questions using simple, transparent keyword rules."""
    text = f"{question} {topic} {category}".lower()

    behavioral_phrases = [
        "tell me about a time",
        "describe a time",
        "give me an example of a time",
        "difficult technical problem",
        "technical challenge",
        "conflict",
        "failure",
        "mistake",
        "leadership",
        "teamwork",
        "how did you handle",
        "what did you do when",
        "how have you dealt with",
        "a challenge you faced",
        "a problem you solved",
    ]

    if any(phrase in text for phrase in behavioral_phrases):
        return "Behavioral"

    return "Technical"


def evaluate_answer(answer, question="", topic="", category=""):
    """
    Evaluate answer structure with transparent rules.
    This is not a semantic correctness or AI evaluation.
    """
    question_type = detect_question_type(question, topic, category)

    if not isinstance(answer, str):
        answer = ""

    answer = answer.strip()

    if question_type == "Behavioral":
        suggested_structure = [
            "Situation: briefly explain the context.",
            "Task: describe your responsibility or goal.",
            "Action: explain the specific steps you personally took.",
            "Result: describe the outcome, using measurable results if possible.",
            "Learning: mention what you learned, if relevant.",
        ]
    else:
        suggested_structure = [
            "Start with a clear definition or direct answer.",
            "Explain the key technical details and how the concept works.",
            "Give a practical example, application, or project experience.",
            "Conclude with a benefit, limitation, or technical trade-off.",
        ]

    if not answer:
        return {
            "score": 0,
            "level": "No answer",
            "word_count": 0,
            "question_type": question_type,
            "strengths": [],
            "improvements": [
                "Write an answer before requesting an evaluation."
            ],
            "suggested_structure": suggested_structure,
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
    answer_lower = answer.lower()

    # 1. Completeness
    if word_count >= 80:
        score += 30
        strengths.append("Your answer provides a reasonable amount of detail.")
    elif word_count >= 40:
        score += 22
        strengths.append("Your answer has a useful starting level of detail.")
    elif word_count >= 20:
        score += 14
        improvements.append(
            "Add more explanation and relevant details."
        )
    else:
        score += 5
        improvements.append(
            "Expand your answer with a clear explanation and supporting details."
        )

    # 2. Structure
    if len(sentences) >= 4:
        score += 20
        strengths.append("Your answer uses several sentences to explain the idea.")
    elif len(sentences) >= 2:
        score += 14
        strengths.append("Your answer has some explanatory structure.")
    else:
        score += 5
        improvements.append("Organize your answer into a few clear sentences.")

    # 3. Question-type-specific evidence
    if question_type == "Behavioral":
        star_indicators = {
            "situation": ["at my", "during", "when i", "in my"],
            "task": ["my task", "i was responsible", "my responsibility", "goal was"],
            "action": ["i decided", "i implemented", "i developed", "i coordinated",
                       "i analyzed", "i created", "i worked", "i took"],
            "result": ["as a result", "the result", "we achieved", "this improved",
                       "i learned", "outcome", "%"],
        }

        found_sections = [
            section
            for section, phrases in star_indicators.items()
            if any(phrase in answer_lower for phrase in phrases)
        ]

        if len(found_sections) >= 3:
            score += 25
            strengths.append(
                "Your answer contains indicators of multiple STAR sections."
            )
        else:
            missing_sections = [
                section.title()
                for section in ["situation", "task", "action", "result"]
                if section not in found_sections
            ]
            improvements.append(
                "Strengthen the STAR structure. Add or clarify: "
                + ", ".join(missing_sections)
                + "."
            )

        if any(
            phrase in answer_lower
            for phrase in ["i ", "my ", "i'm", "i was", "i have"]
        ):
            score += 25
            strengths.append(
                "Your answer includes first-person wording about your contribution."
            )
        else:
            improvements.append(
                "Clarify your personal contribution using specific actions you took."
            )

    else:
        example_phrases = [
            "for example", "for instance", "such as",
            "in practice", "in a project", "we can use",
            "used to", "application"
        ]

        if any(phrase in answer_lower for phrase in example_phrases):
            score += 25
            strengths.append("You included an example or practical application.")
        else:
            improvements.append(
                "Include a practical example or real-world application."
            )

        reasoning_phrases = [
            "because", "therefore", "however", "which means",
            "as a result", "the reason", "in contrast",
            "this helps", "this allows"
        ]

        if any(phrase in answer_lower for phrase in reasoning_phrases):
            score += 25
            strengths.append(
                "You attempted to explain reasoning or relationships."
            )
        else:
            improvements.append(
                "Explain why the concept works and when it is useful."
            )

    # Keep scores capped for short answers.
    score = min(score, 100)

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
            "Add precise details and verify that your claims are accurate."
        )

    return {
        "score": score,
        "level": level,
        "word_count": word_count,
        "question_type": question_type,
        "strengths": strengths,
        "improvements": improvements,
        "suggested_structure": suggested_structure,
    }
