from src.utils.matching_utils import compare_skills

resume = ["Python", "SQL", "Machine Learning"]

job = ["Python", "SQL", "Deep Learning", "Docker"]

result = compare_skills(resume, job)

print(result)