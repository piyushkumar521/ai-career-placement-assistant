
def prioritize_missing_skills(missing_skills):
    """
    Assign learning priorities to missing skills.
    """

    high_priority = [
        "Python",
        "Machine Learning",
        "SQL",
        "Deep Learning"
    ]

    medium_priority = [
        "Generative AI",
        "LLM",
        "RAG",
        "PyTorch",
        "TensorFlow",
        "Scikit-learn",
        "NLP",
        "Computer Vision"
    ]

    recommendations = []

    for skill in missing_skills:
        if skill.lower() in [
            item.lower() for item in high_priority
        ]:
            priority = "High"
        elif skill.lower() in [
            item.lower() for item in medium_priority
        ]:
            priority = "Medium"
        else:
            priority = "Normal"

        recommendations.append({
            "skill": skill,
            "priority": priority,
            "recommendation": (
                f"Start learning {skill} with "
                "fundamentals, then practice through "
                "a small project."
            )
        })

    priority_order = {
        "High": 0,
        "Medium": 1,
        "Normal": 2
    }

    recommendations.sort(
        key=lambda item: priority_order[item["priority"]]
    )

    return recommendations
