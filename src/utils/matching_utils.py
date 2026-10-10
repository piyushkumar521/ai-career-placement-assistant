
def compare_skills(resume_skills, required_skills):
    """
    Compare resume skills with job requirements.
    """

    # Normalize skills for comparison
    resume_set = {
        skill.strip().lower()
        for skill in resume_skills
    }

    required_set = {
        skill.strip().lower()
        for skill in required_skills
    }

    # Find matched and missing skills
    matched = resume_set & required_set
    missing = required_set - resume_set

    # Calculate match percentage
    if required_set:
        match_percentage = (
            len(matched) / len(required_set)
        ) * 100
    else:
        match_percentage = 0

    return {
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "match_percentage": round(match_percentage, 2)
    }
