from src.utils.priority_utils import (
    prioritize_missing_skills
)

missing = [
    "Docker",
    "Deep Learning",
    "RAG",
    "SQL"
]

result = prioritize_missing_skills(missing)

for item in result:
    print(item)