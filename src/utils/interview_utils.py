
import random


SKILL_QUESTIONS = {
    "python": [
        ("Fundamentals", "Explain Python lists, tuples, sets, and dictionaries. When would you use each?"),
        ("Practical", "How would you handle missing values or invalid input in a Python program?"),
        ("Scenario", "Your Python script is running slowly on a large dataset. How would you investigate and improve it?"),
    ],
    "sql": [
        ("Fundamentals", "Explain the difference between WHERE and HAVING in SQL."),
        ("Practical", "Write a query to find the second-highest salary in an employee table."),
        ("Scenario", "A SQL query is slow on a large table. How would you investigate and optimize it?"),
    ],
    "machine learning": [
        ("Fundamentals", "Explain the difference between supervised and unsupervised learning."),
        ("Practical", "How would you select an appropriate evaluation metric for a classification model?"),
        ("Scenario", "Your model performs well on training data but poorly on unseen data. How would you address this?"),
    ],
    "deep learning": [
        ("Fundamentals", "What is backpropagation, and why is it needed when training neural networks?"),
        ("Practical", "What are epochs, batches, and learning rate in neural network training?"),
        ("Scenario", "A neural network's training loss stops improving. What would you investigate?"),
    ],
    "generative ai": [
        ("Fundamentals", "What is Generative AI, and how does it differ from traditional machine learning?"),
        ("Practical", "What is prompt engineering, and how can you improve an unreliable model response?"),
        ("Scenario", "How would you design a Generative AI assistant that answers questions using company documents?"),
    ],
    "llm": [
        ("Fundamentals", "What is a large language model, and what is tokenization?"),
        ("Practical", "What is the difference between prompting and fine-tuning an LLM?"),
        ("Scenario", "An LLM produces incorrect answers. How would you reduce hallucinations?"),
    ],
    "rag": [
        ("Fundamentals", "Explain the main stages of a Retrieval-Augmented Generation (RAG) pipeline."),
        ("Practical", "Why are documents split into chunks before creating embeddings?"),
        ("Scenario", "A RAG application retrieves irrelevant passages. How would you debug and improve retrieval?"),
    ],
    "docker": [
        ("Fundamentals", "What is Docker, and how is a container different from a virtual machine?"),
        ("Practical", "What is a Dockerfile, and how would you build an image for a Python application?"),
        ("Scenario", "Your application works locally but fails inside a container. How would you troubleshoot it?"),
    ],
    "streamlit": [
        ("Fundamentals", "How does Streamlit help you build interactive Python applications?"),
        ("Practical", "What is Streamlit session state, and when would you use it?"),
        ("Scenario", "A user's uploaded data disappears after navigating between pages. How would you investigate?"),
    ],
    "fastapi": [
        ("Fundamentals", "What is FastAPI, and how does it differ from a traditional web framework?"),
        ("Practical", "How would you create a POST endpoint that accepts JSON input?"),
        ("Scenario", "How would you validate incoming data and return useful errors from an API?"),
    ],
    "nlp": [
        ("Fundamentals", "What is the difference between stemming and lemmatization?"),
        ("Practical", "How would you convert text into numerical features for a machine learning model?"),
        ("Scenario", "How would you prepare a text classification model when the classes are imbalanced?"),
    ],
    "computer vision": [
        ("Fundamentals", "What is a convolutional neural network, and why is it useful for images?"),
        ("Practical", "Why might image normalization and data augmentation be useful?"),
        ("Scenario", "An image classifier performs poorly on images from a new camera. What would you investigate?"),
    ],
    "pytorch": [
        ("Fundamentals", "What is a tensor in PyTorch, and how is it used in deep learning?"),
        ("Practical", "Describe the basic training loop for a PyTorch model."),
        ("Scenario", "Your model's gradients become very large during training. What might you try?"),
    ],
    "tensorflow": [
        ("Fundamentals", "What are tensors and Keras in the TensorFlow ecosystem?"),
        ("Practical", "Describe the steps to build, compile, and train a model using Keras."),
        ("Scenario", "A TensorFlow model overfits its training data. Which techniques could help?"),
    ],
    "scikit-learn": [
        ("Fundamentals", "What is the purpose of scikit-learn in a machine learning workflow?"),
        ("Practical", "Why should preprocessing and model training often be combined in a Pipeline?"),
        ("Scenario", "How would you use cross-validation to compare two candidate models?"),
    ],
    "data science": [
        ("Fundamentals", "Explain the main stages of a typical data science project."),
        ("Practical", "How would you identify and handle outliers in a dataset?"),
        ("Scenario", "A dataset contains missing values, inconsistent formats, and duplicate rows. How would you prepare it for analysis?"),
    ],
    "langchain": [
        ("Fundamentals", "What problems can LangChain help solve in LLM applications?"),
        ("Practical", "How can a prompt template and an LLM be connected in an application?"),
        ("Scenario", "How would you debug a chain that produces incomplete or irrelevant answers?"),
    ],
    "langgraph": [
        ("Fundamentals", "What is LangGraph, and why might an application need a graph-based workflow?"),
        ("Practical", "Explain nodes, edges, and state in a LangGraph workflow."),
        ("Scenario", "How could you design an agent workflow that retries a failed tool call safely?"),
    ],
}


ROLE_QUESTIONS = {
    "ece": [
        "Explain the difference between analog and digital signals.",
        "What is the difference between a microprocessor and a microcontroller?",
        "Explain the basic working of a MOSFET.",
        "What is the purpose of a flip-flop in a digital circuit?",
        "Explain the difference between combinational and sequential circuits.",
    ],
    "software": [
        "Explain the difference between a process and a thread.",
        "What is the difference between a stack and a queue?",
        "How would you debug a program that produces an unexpected result?",
        "Explain the time complexity of binary search.",
    ],
    "data": [
        "How would you explain a business insight discovered from a dataset?",
        "What is the difference between correlation and causation?",
        "How would you validate that a dataset is suitable for analysis?",
    ],
    "general": [
        "Walk me through a technical project you have completed.",
        "What was a difficult technical problem you faced, and how did you solve it?",
        "How do you learn a new technology and verify your understanding?",
        "Explain a technical concept from your resume to a beginner.",
    ],
}


def generate_interview_questions(
    target_role,
    resume_skills,
    required_skills,
    missing_skills,
    categories,
    num_questions=10,
):
    """Generate a reproducible-style practice set from available skill data."""
    target_role = target_role.strip() or "General Technical Role"

    # Prioritize missing skills, then skills mentioned in the job description
    # and resume.
    skill_order = []
    for skill in list(missing_skills) + list(required_skills) + list(resume_skills):
        normalized = skill.strip().lower()
        if normalized and normalized not in skill_order:
            skill_order.append(normalized)

    pool = []
    for skill in skill_order:
        for category, question in SKILL_QUESTIONS.get(skill, []):
            if not categories or category in categories:
                pool.append({
                    "question": question,
                    "topic": skill.title(),
                    "category": category,
                })

    role = target_role.lower()
    if any(term in role for term in ["ece", "electronics", "embedded", "vlsi", "hardware"]):
        role_questions = ROLE_QUESTIONS["ece"]
    elif any(term in role for term in ["software", "developer", "programmer", "backend"]):
        role_questions = ROLE_QUESTIONS["software"]
    elif any(term in role for term in ["data", "machine learning", "ai", "ml"]):
        role_questions = ROLE_QUESTIONS["data"]
    else:
        role_questions = ROLE_QUESTIONS["general"]

    if not categories or "Role-specific" in categories:
        for question in role_questions:
            pool.append({
                "question": question,
                "topic": target_role,
                "category": "Role-specific",
            })

    # Add general questions to ensure there are enough questions to choose from.
    for question in ROLE_QUESTIONS["general"]:
        pool.append({
            "question": question,
            "topic": "General Interview",
            "category": "General",
        })

    # Remove duplicate questions while preserving order.
    unique_pool = []
    seen = set()
    for item in pool:
        if item["question"] not in seen:
            unique_pool.append(item)
            seen.add(item["question"])

    random.shuffle(unique_pool)
    selected = unique_pool[:max(1, min(int(num_questions), len(unique_pool)))]

    # Put questions about skill gaps first.
    missing = {skill.lower() for skill in missing_skills}
    selected.sort(key=lambda item: 0 if item["topic"].lower() in missing else 1)

    return selected
