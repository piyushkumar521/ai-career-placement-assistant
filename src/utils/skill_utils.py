def extract_skills(text):

    skills = [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "SQL",
        "Data Science",
        "Generative AI",
        "LLM",
        "RAG",
        "LangChain",
        "LangGraph",
        "Docker",
        "Streamlit",
        "FastAPI",
        "PyTorch",
        "TensorFlow",
        "Scikit-learn",
        "NLP",
        "Computer Vision"
    ]

    detected_skills = []

    normalized_text = text.lower()
    normalized_text = normalized_text.replace("-", " ")

    for skill in skills:

        normalized_skill = (
            skill.lower().replace("-", " ")
        )

        if normalized_skill in normalized_text:
            detected_skills.append(skill)

    return detected_skills