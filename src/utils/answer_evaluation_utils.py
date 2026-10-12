
import re


def get_topic_guidance(question="", topic="", category=""):
    """Return rule-based guidance for common technical topics."""
    text = f"{question} {topic} {category}".lower()

    topic_rules = [
        (
            [
                "python", "list", "tuple", "dictionary", "dict", "set",
                "function", "exception", "oop", "class", "inheritance",
            ],
            "Python",
            [
                "Explain the relevant Python concept and its syntax.",
                "Mention an important property or difference from related concepts.",
                "Include a short Python code example and explain its output.",
            ],
        ),
        (
            [
                "sql", "database", "join", "where", "having", "group by",
                "primary key", "foreign key", "query",
            ],
            "SQL",
            [
                "Explain the SQL clause or database concept clearly.",
                "Describe when it is used and how it differs from related concepts.",
                "Include a small SQL query and explain the expected result.",
            ],
        ),
        (
            [
                "machine learning", "overfitting", "underfitting",
                "regression", "classification", "random forest",
                "decision tree", "precision", "recall", "f1 score",
                "feature engineering", "supervised learning",
                "unsupervised learning",
            ],
            "Machine Learning",
            [
                "Define the concept and explain how it works.",
                "Describe a suitable use case, limitation, or trade-off.",
                "Give an example and mention a relevant evaluation method when appropriate.",
            ],
        ),
        (
            [
                "deep learning", "neural network", "backpropagation",
                "activation function", "epoch", "gradient descent",
                "cnn", "rnn", "transformer", "loss function",
            ],
            "Deep Learning",
            [
                "Explain the neural-network concept and its purpose.",
                "Describe the main mechanism or training process.",
                "Give an application and mention a relevant limitation when appropriate.",
            ],
        ),
    ]

    for keywords, topic_name, guidance in topic_rules:
        if any(keyword in text for keyword in keywords):
            return {
                "topic_name": topic_name,
                "guidance": guidance,
            }

    return {
        "topic_name": "General",
        "guidance": [
            "Define the main concept clearly.",
            "Explain how it works and why it is useful.",
            "Include a practical example and mention a limitation when relevant.",
        ],
    }


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
    Evaluate answer structure using transparent rules.

    This is a practice aid, not a semantic correctness or AI evaluation.
    """
    question_type = detect_question_type(question, topic, category)
    topic_result = get_topic_guidance(question, topic, category)

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

        # Add topic-specific suggestions for technical questions.
        suggested_structure.extend(topic_result["guidance"])

    if not answer:
        return {
            "score": 0,
            "level": "No answer",
            "word_count": 0,
            "question_type": question_type,
            "topic_name": topic_result["topic_name"],
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
        strengths.append(
            "Your answer provides a reasonable amount of detail."
        )
    elif word_count >= 40:
        score += 22
        strengths.append(
            "Your answer has a useful starting level of detail."
        )
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
        strengths.append(
            "Your answer uses several sentences to explain the idea."
        )
    elif len(sentences) >= 2:
        score += 14
        strengths.append(
            "Your answer has some explanatory structure."
        )
    else:
        score += 5
        improvements.append(
            "Organize your answer into a few clear sentences."
        )

    # 3. Question-type-specific evidence
    if question_type == "Behavioral":
        star_indicators = {
            "situation": [
                "at my", "during", "when i", "in my",
            ],
            "task": [
                "my task", "i was responsible",
                "my responsibility", "goal was",
            ],
            "action": [
                "i decided", "i implemented", "i developed",
                "i coordinated", "i analyzed", "i created",
                "i worked", "i took",
            ],
            "result": [
                "as a result", "the result", "we achieved",
                "this improved", "i learned", "outcome", "%",
            ],
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
        # 4. Examples and applications
        example_phrases = [
            "for example", "for instance", "such as",
            "in practice", "in a project", "we can use",
            "used to", "application",
        ]

        if any(phrase in answer_lower for phrase in example_phrases):
            score += 25
            strengths.append(
                "You included an example or practical application."
            )
        else:
            improvements.append(
                "Include a practical example or real-world application."
            )

        # 5. Explanation and reasoning
        reasoning_phrases = [
            "because", "therefore", "however", "which means",
            "as a result", "the reason", "in contrast",
            "this helps", "this allows",
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

    # Limit scores for answers that are too short.
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
        "topic_name": topic_result["topic_name"],
        "strengths": strengths,
        "improvements": improvements,
        "suggested_structure": suggested_structure,
    }
