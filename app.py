
import json
import streamlit as st

from src.utils.pdf_utils import extract_text_from_pdf
from src.utils.text_utils import clean_resume_text
from src.utils.jd_utils import process_job_description
from src.utils.skill_utils import extract_skills
from src.utils.matching_utils import compare_skills
from src.utils.priority_utils import prioritize_missing_skills
from src.utils.interview_utils import generate_interview_questions
from src.utils.answer_evaluation_utils import evaluate_answer
from src.utils.semantic_matching_utils import compare_resume_and_job


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Career & Placement Assistant",
    page_icon="🎯",
    layout="wide",
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {
    "resume_text": "",
    "resume_skills": [],
    "resume_filename": "",
    "jd_text": "",
    "jd_skills": [],
    "jd_filename": "",
    "last_skill_match": {},
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HELPER: PERSONALIZED ROADMAP
# ============================================================

def generate_learning_roadmap(missing_skills):
    learning_paths = {
        "python": (
            "4 days",
            ["Data types and variables", "Conditions and loops",
             "Functions and collections", "Practice coding problems"],
            "Build a Python expense tracker",
        ),
        "sql": (
            "4 days",
            ["SELECT and WHERE", "Aggregate functions and GROUP BY",
             "JOINs and subqueries", "Practice interview questions"],
            "Analyze a sales database",
        ),
        "machine learning": (
            "7 days",
            ["Supervised and unsupervised learning",
             "Data preprocessing", "Regression and classification",
             "Model evaluation", "Decision trees and ensembles",
             "Overfitting and regularization", "Model practice"],
            "Build a customer churn prediction model",
        ),
        "deep learning": (
            "7 days",
            ["Neural network fundamentals", "Activation and loss functions",
             "Forward and backward propagation", "Optimizers",
             "Training and validation", "Introduction to CNNs",
             "Practice a neural network"],
            "Build a handwritten digit classifier",
        ),
        "generative ai": (
            "5 days",
            ["Generative AI fundamentals", "LLM and transformer basics",
             "Prompt engineering", "LLM API usage",
             "Build a simple AI application"],
            "Create an AI text summarizer",
        ),
        "llm": (
            "5 days",
            ["Transformer fundamentals", "Tokens and embeddings",
             "Context windows", "Prompting and structured outputs",
             "LLM application development"],
            "Build a question-answering chatbot",
        ),
        "rag": (
            "5 days",
            ["RAG fundamentals", "Document chunking",
             "Embeddings", "Vector search", "Retrieval and generation"],
            "Build a PDF question-answering assistant",
        ),
        "docker": (
            "3 days",
            ["Containers and images", "Writing a Dockerfile",
             "Building and running containers"],
            "Containerize a Python application",
        ),
        "streamlit": (
            "3 days",
            ["Widgets and layouts", "Session state",
             "Displaying results and downloads"],
            "Build an interactive ML dashboard",
        ),
        "fastapi": (
            "4 days",
            ["REST API fundamentals", "Endpoints",
             "Request validation", "Testing API endpoints"],
            "Create an ML prediction API",
        ),
        "nlp": (
            "5 days",
            ["Text preprocessing", "Tokenization and vectorization",
             "Text classification", "Evaluation metrics", "Pipeline practice"],
            "Build a sentiment classifier",
        ),
        "computer vision": (
            "5 days",
            ["Image preprocessing", "Image augmentation",
             "Convolutional neural networks", "Image classification",
             "Model evaluation"],
            "Build an image classification application",
        ),
        "pytorch": (
            "4 days",
            ["Tensors", "Datasets and data loaders",
             "Neural network construction", "Training loops"],
            "Train a neural network using PyTorch",
        ),
        "tensorflow": (
            "4 days",
            ["Tensors", "Keras models", "Training and validation",
             "Model evaluation"],
            "Build a TensorFlow classification model",
        ),
        "scikit-learn": (
            "4 days",
            ["Estimators", "Preprocessing pipelines",
             "Cross-validation", "Model evaluation and tuning"],
            "Build an end-to-end ML pipeline",
        ),
        "data science": (
            "5 days",
            ["Data cleaning", "Exploratory data analysis",
             "Visualization", "Statistics", "Communicating insights"],
            "Analyze a real-world dataset",
        ),
        "langchain": (
            "4 days",
            ["Prompt templates", "Chains and output parsing",
             "Document loaders", "Retrievers"],
            "Build a document-based AI assistant",
        ),
        "langgraph": (
            "4 days",
            ["Graph and state fundamentals", "Nodes and edges",
             "Conditional routing", "Agent workflow"],
            "Build a multi-step AI assistant",
        ),
    }

    roadmap = []

    for skill in missing_skills:
        path = learning_paths.get(skill.strip().lower())

        if path is None:
            path = (
                "2 days",
                [
                    f"Learn the fundamentals of {skill}",
                    f"Practice {skill} through hands-on exercises",
                ],
                f"Build a small project using {skill}",
            )

        duration, topics, project = path

        roadmap.append({
            "skill": skill,
            "duration": duration,
            "topics": topics,
            "project": project,
        })

    return roadmap


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎯 Career Assistant")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",
        "📄 Resume Analysis",
        "💼 Job Description",
        "📊 Skill Gap Analysis",
        "🗺️ Career Roadmap",
        "🎤 Interview Assistant",
    ],
)

st.sidebar.divider()
st.sidebar.markdown("### 👨‍💻 PIYUSH KUMAR YADAV")
st.sidebar.caption("AI/ML Engineer")


# ============================================================
# MAIN TITLE
# ============================================================

st.title("🎯 AI Career & Placement Assistant")
st.write("Your AI-powered career and placement companion.")


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.subheader("Welcome 👋")

    resume_saved = bool(st.session_state["resume_text"])
    jd_saved = bool(st.session_state["jd_text"])

    last_result = st.session_state.get("last_skill_match", {})

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📄 Resume",
        "Processed" if resume_saved else "Not Processed",
    )
    col2.metric(
        "💼 Job Description",
        "Processed" if jd_saved else "Not Processed",
    )
    col3.metric(
        "📊 Skills Matched",
        len(last_result.get("matched_skills", [])),
    )
    col4.metric(
        "🎯 Readiness Score",
        f"{last_result.get('match_percentage', 0)}%",
    )

    st.divider()

    st.subheader("🚀 What You Can Do")

    st.info(
        "Process your resume and target job description to explore "
        "skill matching, learning priorities, a career roadmap, "
        "and interview preparation."
    )

    if resume_saved:
        st.success(
            f"Resume data saved: "
            f"{st.session_state['resume_filename'] or 'Resume'}"
        )

    if jd_saved:
        st.success(
            f"Job description saved: "
            f"{st.session_state['jd_filename'] or 'Job description'}"
        )


# ============================================================
# RESUME ANALYSIS
# ============================================================

elif page == "📄 Resume Analysis":

    st.header("📄 Resume Analysis")

    st.write("Upload your resume in PDF format.")

    uploaded_resume = st.file_uploader(
        "Upload your Resume",
        type=["pdf"],
        key="resume_pdf_uploader",
    )

    if uploaded_resume is not None:

        try:
            uploaded_resume.seek(0)
            raw_text = extract_text_from_pdf(uploaded_resume)
            cleaned_text = clean_resume_text(raw_text)
            detected_skills = extract_skills(cleaned_text)

            st.session_state["resume_text"] = cleaned_text
            st.session_state["resume_skills"] = detected_skills
            st.session_state["resume_filename"] = uploaded_resume.name
            st.session_state.pop("last_skill_match", None)

            st.success("✅ Resume processed successfully!")

        except Exception as error:
            st.error(f"Could not process resume: {error}")

    # Always display previously processed data.
    if st.session_state["resume_text"]:

        resume_text = st.session_state["resume_text"]
        resume_skills = st.session_state["resume_skills"]

        st.subheader("💾 Saved Resume")

        st.write(
            "**File:**",
            st.session_state["resume_filename"] or "Resume",
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Words", len(resume_text.split()))
        col2.metric("Skills Detected", len(resume_skills))
        col3.metric("Lines", len(resume_text.splitlines()))

        if resume_skills:
            st.success(", ".join(resume_skills))
        else:
            st.warning(
                "No supported skills were detected. "
                "Check the PDF text and supported skill keywords."
            )

        with st.expander("View Extracted Resume Text"):
            st.text_area(
                "Saved Resume Text",
                resume_text,
                height=300,
                key="resume_saved_preview",
            )

    else:
        st.info("Upload and process a resume to get started.")


# ============================================================
# JOB DESCRIPTION
# ============================================================

elif page == "💼 Job Description":

    st.header("💼 Job Description")

    st.write("Paste a job description or upload it as a PDF.")

    st.subheader("📝 Paste Job Description")

    # Use a separate widget key from the saved processed text.
    jd_input = st.text_area(
        "Paste Job Description",
        height=220,
        placeholder="Paste the complete job description here...",
        key="jd_text_input",
    )

    if st.button("🔍 Process Job Description"):

        if jd_input.strip():

            cleaned_jd = process_job_description(jd_input)
            required_skills = extract_skills(cleaned_jd)

            st.session_state["jd_text"] = cleaned_jd
            st.session_state["jd_skills"] = required_skills
            st.session_state["jd_filename"] = "Pasted job description"
            st.session_state.pop("last_skill_match", None)

            st.success("✅ Job description processed successfully!")

        else:
            st.warning("Please paste a job description first.")

    st.divider()
    st.write("**OR upload a PDF**")

    uploaded_jd = st.file_uploader(
        "Upload Job Description PDF",
        type=["pdf"],
        key="jd_pdf_uploader",
    )

    if uploaded_jd is not None:

        try:
            uploaded_jd.seek(0)
            raw_jd = extract_text_from_pdf(uploaded_jd)
            cleaned_jd = process_job_description(raw_jd)

            st.session_state["jd_text"] = cleaned_jd
            st.session_state["jd_skills"] = extract_skills(cleaned_jd)
            st.session_state["jd_filename"] = uploaded_jd.name
            st.session_state.pop("last_skill_match", None)

            st.success("✅ Job description PDF processed successfully!")

        except Exception as error:
            st.error(f"Could not process job description: {error}")

    # Display saved job description, even after page navigation.
    if st.session_state["jd_text"]:

        st.divider()
        st.subheader("💾 Saved Job Description")

        st.write(
            "**File/source:**",
            st.session_state["jd_filename"] or "Job description",
        )

        saved_jd_skills = st.session_state["jd_skills"]

        if saved_jd_skills:
            st.success(", ".join(saved_jd_skills))
        else:
            st.warning(
                "No supported skills were detected in this job description."
            )

        with st.expander("View Saved Job Description Text"):
            st.text_area(
                "Saved JD Text",
                st.session_state["jd_text"],
                height=300,
                key="jd_saved_preview",
            )

    else:
        st.info("Add and process a job description to continue.")


# ============================================================
# SKILL GAP ANALYSIS AND DOWNLOAD REPORT
# ============================================================

elif page == "📊 Skill Gap Analysis":

    st.header("📊 Skill Gap Analysis")
    
    
    st.divider()
    st.subheader("🧠 Semantic Resume–Job Similarity")

    resume_text = st.session_state.get("resume_text", "")
    job_text = st.session_state.get("jd_text", "")

    if resume_text.strip() and job_text.strip():
        if st.button("Calculate Semantic Similarity"):
            with st.spinner("Comparing resume and job description..."):
                try:
                    semantic_result = compare_resume_and_job(
                        resume_text,
                        job_text,
                    )

                    st.metric(
                        "Semantic Similarity Indicator",
                        f"{semantic_result['semantic_similarity_score']}/100",
                    )

                    st.caption(
                        "This score measures text similarity. It is not a "
                        "job-fit percentage or a hiring probability."
                    )

                    st.write(
                        "Cosine similarity:",
                        semantic_result["cosine_similarity"],
                    )

                except Exception as error:
                    st.error(f"Semantic comparison failed: {error}")
        else:
            st.info(
                "Process a resume and a job description before calculating "
                "semantic similarity."
            )

    resume_text = st.session_state.get("resume_text", "")
    jd_text = st.session_state.get("jd_text", "")

    resume_skills = st.session_state.get("resume_skills", [])
    required_skills = st.session_state.get("jd_skills", [])

    if not resume_text or not jd_text:

        st.warning(
            "Please process both your resume and job description first."
        )

        st.write(
            f"Resume processed: {'Yes' if resume_text else 'No'}"
        )
        st.write(
            f"Job description processed: {'Yes' if jd_text else 'No'}"
        )

    else:

        # Analyze even if one document has no detected skills.
        result = compare_skills(resume_skills, required_skills)

        matched = result["matched_skills"]
        missing = result["missing_skills"]
        percentage = result["match_percentage"]

        st.session_state["last_skill_match"] = result

        col1, col2, col3 = st.columns(3)

        col1.metric("Match Percentage", f"{percentage}%")
        col2.metric("Matched Skills", len(matched))
        col3.metric("Missing Skills", len(missing))

        st.progress(int(percentage))

        st.subheader("📄 Analysis Summary")

        st.write(f"Resume skills detected: {len(resume_skills)}")
        st.write(f"Job skills detected: {len(required_skills)}")

        if not resume_skills:
            st.warning(
                "No supported skills were detected in your resume. "
                "The match percentage may not be meaningful."
            )

        if not required_skills:
            st.warning(
                "No supported skills were detected in the job description. "
                "The match percentage may not be meaningful."
            )

        st.subheader("✅ Matched Skills")

        if matched:
            st.success(", ".join(matched))
        else:
            st.info("No matching skills found.")

        st.subheader("❌ Missing Skills")

        recommendations = []

        if missing:

            st.error(", ".join(missing))

            recommendations = prioritize_missing_skills(missing)

            st.subheader("🎯 Recommended Learning Priorities")

            for item in recommendations:
                st.markdown(
                    f"**{item['skill']}** — Priority: {item['priority']}"
                )
                st.write(item["recommendation"])

        elif required_skills:
            st.success("All detected job-description skills are matched!")

        # ----------------------------------------------------
        # DOWNLOAD REPORT
        report = {
            "resume_filename": st.session_state.get(
                "resume_filename", ""
            ),
            "job_description_filename": st.session_state.get(
                "jd_filename", ""
            ),
            "resume_skills": resume_skills,
            "required_skills": required_skills,
            "match_percentage": percentage,
            "matched_skills": matched,
            "missing_skills": missing,
            "learning_priorities": recommendations,
        }

        report_json = json.dumps(report, indent=4)

        st.divider()
        st.subheader("📥 Download Skill Gap Report")

        st.download_button(
            label="⬇️ Download Report (JSON)",
            data=report_json,
            file_name="skill_gap_report.json",
            mime="application/json",
            key="download_skill_gap_report",
        )


# ============================================================
# CAREER ROADMAP
# ============================================================

elif page == "🗺️ Career Roadmap":

    st.header("🗺️ Personalized Career Roadmap")

    resume_text = st.session_state.get("resume_text", "")
    jd_text = st.session_state.get("jd_text", "")

    resume_skills = st.session_state.get("resume_skills", [])
    required_skills = st.session_state.get("jd_skills", [])

    if not resume_text or not jd_text:

        st.warning(
            "Process your resume and job description before "
            "generating a personalized roadmap."
        )

    else:

        result = compare_skills(resume_skills, required_skills)
        missing = result["missing_skills"]

        st.metric(
            "Current Job Skill Match",
            f"{result['match_percentage']}%",
        )

        if not required_skills:

            st.warning(
                "No supported skills were detected in the job description. "
                "Check its content before creating a roadmap."
            )

        elif not missing:

            st.success(
                "🎉 All detected job-description skills are present "
                "in your resume!"
            )

            st.info(
                "Continue with advanced practice, projects, "
                "and interview preparation."
            )

        else:

            roadmap = generate_learning_roadmap(missing)

            st.subheader("🎯 Recommended Learning Plan")

            for index, item in enumerate(roadmap, start=1):

                with st.expander(
                    f"{index}. {item['skill']} — {item['duration']}"
                ):

                    st.write("**Topics to learn:**")

                    for topic_index, topic in enumerate(
                        item["topics"], start=1
                    ):
                        st.checkbox(
                            topic,
                            key=f"roadmap_{index}_{topic_index}",
                        )

                    st.write("**Hands-on project:**")
                    st.info(item["project"])

            st.caption(
                "Durations are estimates. Actual completion time "
                "depends on your experience and daily practice."
            )


# ============================================================
# INTERVIEW ASSISTANT
# ============================================================

elif page == "🎤 Interview Assistant":
    st.title("🎤 Personalized Interview Assistant")
    st.write(
        "Generate practice questions based on your target role, "
        "job description, resume skills, and skill gaps."
    )

    target_role = st.text_input(
        "Target Job Role",
        value="AI/ML Engineer",
        key="interview_target_role",
        placeholder="e.g., ECE Engineer, VLSI Engineer, Data Analyst",
    )

    categories = st.multiselect(
        "Question Categories",
        options=[
            "Fundamentals",
            "Practical",
            "Scenario",
            "Role-specific",
        ],
        default=["Fundamentals", "Practical", "Scenario", "Role-specific"],
        key="interview_categories",
    )

    num_questions = st.slider(
        "Number of Questions",
        min_value=5,
        max_value=20,
        value=10,
        key="interview_num_questions",
    )
    
    difficulty = st.selectbox(
        "Question Difficulty",
        ["Beginner", "Intermediate", "Advanced"],
        index=1,
        help="Choose the difficulty level for your interview practice.",
    )
    

    if st.button("🚀 Generate Interview Questions", type="primary"):
        if not target_role.strip():
            st.warning("Please enter a target job role.")
        else:
            resume_skills = st.session_state.get("resume_skills", [])
            required_skills = st.session_state.get("jd_skills", [])

            result = st.session_state.get("last_skill_match", {})
            missing_skills = result.get("missing_skills", [])

            questions = generate_interview_questions(
                target_role=target_role,
                resume_skills=resume_skills,
                required_skills=required_skills,
                missing_skills=missing_skills,
                categories=categories,
                num_questions=num_questions,
                difficulty=difficulty,
            )

            st.session_state["generated_interview_questions"] = questions

            # Clear old evaluations when generating a new question set.
            for key in list(st.session_state.keys()):
                if key.startswith("evaluation_"):
                    del st.session_state[key]

    questions = st.session_state.get("generated_interview_questions", [])

    if questions:
        st.divider()
        st.subheader(
            f"Your Interview Practice Set ({len(questions)} questions)"
        )

        for index, item in enumerate(questions, start=1):
            with st.expander(
                f"Q{index}. [{item['category']}] {item['topic']}"
            ):
                st.caption(
                    f"Difficulty: {item.get('difficulty', 'Intermediate')}"
                )
                st.write(item["question"])

                answer_key = f"interview_answer_{index}"
                answer = st.text_area(
                    "Your answer",
                    key=answer_key,
                    placeholder="Write your answer here...",
                )

                if st.button(
                    "📝 Evaluate My Answer",
                    key=f"evaluate_answer_{index}",
                ):
                    evaluation = evaluate_answer(
                        answer=answer,
                        question=item["question"],
                        topic=item["topic"],
                        category=item["category"],
                    )

                    # Save the evaluation so it survives Streamlit reruns.
                    st.session_state[f"evaluation_{index}"] = evaluation

                evaluation = st.session_state.get(f"evaluation_{index}")

                if evaluation is not None:
                    st.divider()
                    st.subheader("Answer Feedback")

                    st.metric(
                        "Practice Score (Structure Only)",
                        f"{evaluation.get('score', 0)}/100",
                    )

                    st.caption(
                        "This rule-based score checks answer length and "
                        "structure; it does not verify technical correctness."
                    )

                    st.write(
                        f"**Assessment:** "
                        f"{evaluation.get('level', 'Not available')}"
                    )
                    
                    
                    st.write(
                       f"**Question Type:** "
                       f"{evaluation.get('question_type', 'Not available')}"
                    )
                    
                    st.write(
                        f"**Topic:** "
                        f"{evaluation.get('topic_name', 'General')}"
                    )
                
                    st.write(
                        f"**Word count:** {evaluation.get('word_count', 0)}"
                    )

                    st.write("**Strengths**")
                    strengths = evaluation.get("strengths", [])

                    if strengths:
                        for strength in strengths:
                            st.write(f"✅ {strength}")
                    else:
                        st.write("No strengths identified yet.")

                    st.write("**Areas to improve**")
                    for improvement in evaluation.get("improvements", []):
                        st.write(f"📌 {improvement}")
                        
                    st.write("**Missing Concepts to Consider**")
                    missing_concepts = evaluation.get(
                        "missing_concepts", []
                    )

                    if missing_concepts:
                        for concept in missing_concepts:
                            st.write(f"🔎 {concept}")
                    else:
                        st.write(
                            "No missing concepts detected by the "
                            "current keyword rules."
                        )
                    
                        

                    st.write("**Suggested answer structure**")
                    for point in evaluation.get("suggested_structure", []):
                        st.write(f"- {point}")

        question_text = "\n\n".join(
            f"Q{i}. [{item['category']}] {item['topic']}\n"
            f"{item['question']}"
            for i, item in enumerate(questions, start=1)
        )

        st.download_button(
            "📥 Download Interview Questions",
            data=question_text,
            file_name="interview_practice_questions.txt",
            mime="text/plain",
        )
    else:
        st.info(
            "Choose your preferences and click Generate Interview Questions."
        )
