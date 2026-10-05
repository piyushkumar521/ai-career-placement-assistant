import streamlit as st
from src.utils.pdf_utils import extract_text_from_pdf

st.set_page_config(
    page_title="AI Career & Placement Assistant",
    page_icon="🎯",
    layout="wide"
)

# Sidebar
st.sidebar.title("🎯 Career Assistant")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",
        "📄 Resume Analysis",
        "💼 Job Description",
        "📊 Skill Gap Analysis",
        "🗺️ Career Roadmap",
        "🎤 Interview Assistant"
    ]
)

# Main content
st.title("🎯 AI Career & Placement Assistant")

st.write(
    "Your AI-powered career and placement companion."
)

if page == "🏠 Dashboard":
    st.subheader("Welcome 👋")

    st.write(
        "Your AI-powered career and placement companion."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📄 Resume", "Not Uploaded")

    with col2:
        st.metric("💼 Job Description", "Not Added")

    with col3:
        st.metric("📊 Skills Matched", "0")

    with col4:
        st.metric("🎯 Readiness Score", "0%")

    st.divider()

    st.subheader("🚀 What You Can Do")

    st.info(
        "Upload your resume and job description to get "
        "personalized skill-gap analysis, career planning, "
        "and interview preparation."
    )

elif page == "📄 Resume Analysis":
    st.header("📄 Resume Analysis")

    st.write(
        "Upload your resume in PDF format. "
        "The AI assistant will analyze it in later stages."
    )

    uploaded_resume = st.file_uploader(
        "Upload your Resume",
        type=["pdf"],
        help="Upload your latest resume in PDF format."
    )

    if uploaded_resume is not None:
        st.success("✅ Resume uploaded successfully!")

        st.write("**File name:**", uploaded_resume.name)
        st.write("**File size:**", f"{uploaded_resume.size / 1024:.2f} KB")

        # Extract text from PDF
        resume_text = extract_text_from_pdf(uploaded_resume)
        st.session_state["resume_text"]=resume_text
        st.caption(f"Resume text stored: {len(resume_text)} characters")

        if resume_text.strip():
            st.success("✅ Resume text extracted successfully!")

            with st.expander("📄 View Extracted Resume Text"):
                st.text_area(
                    "Extracted Text",
                    resume_text,
                    height=500
               )
        else:
            st.warning(
                "⚠️ No text could be extracted from this PDF. "
                "It may be a scanned/image-based PDF."
           )

elif page == "💼 Job Description":
    st.header("💼 Job Description")

    st.write(
        "Add the job description you want to analyze."
    )

    jd_text = st.text_area(
        "Paste Job Description",
        height=250,
        placeholder=(
            "Paste the complete job description here..."
        )
    )

    st.write("**OR**")

    uploaded_jd = st.file_uploader(
        "Upload Job Description PDF",
        type=["pdf"],
        help="Upload the job description as a PDF."
    )

    if jd_text.strip():
        st.success("✅ Job description added successfully!")

    if uploaded_jd is not None:
        st.success("✅ Job description PDF uploaded successfully!")

        st.write("**File name:**", uploaded_jd.name)
        st.write(
            "**File size:**",
            f"{uploaded_jd.size / 1024:.2f} KB"
        )

    if not jd_text.strip() and uploaded_jd is None:
        st.info(
            "Paste a job description or upload a PDF "
            "to continue."
        )

elif page == "📊 Skill Gap Analysis":
    st.header("📊 Skill Gap Analysis")

    st.write(
        "Compare your resume skills with the skills "
        "required by the selected job."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matched Skills")

        matched_skills = [
            "Python",
            "Machine Learning",
            "SQL"
        ]

        for skill in matched_skills:
            st.success(skill)

    with col2:
        st.subheader("⚠️ Missing Skills")

        missing_skills = [
            "Deep Learning",
            "Docker",
            "LLM"
        ]

        for skill in missing_skills:
            st.warning(skill)

    st.divider()

    st.subheader("📈 Skill Match")

    st.progress(0.50)

    st.write("Current skill match: **50%**")

    st.info(
        "Actual skill extraction and matching using "
        "AI/RAG will be implemented later."
    )

elif page == "🗺️ Career Roadmap":
    st.header("🗺️ Personalized Career Roadmap")

    st.write(
        "Build a personalized learning path based on "
        "your current skills and career target."
    )

    st.subheader("🎯 Target Role")

    target_role = st.selectbox(
        "Select your target role",
        [
            "AI/ML Engineer",
            "Data Scientist",
            "GenAI Engineer",
            "ML Engineer"
        ]
    )

    st.success(f"Selected target: **{target_role}**")

    st.divider()

    st.subheader("🛣️ Learning Roadmap")

    roadmap = [
        ("1️⃣", "Python & Data Science", "Completed"),
        ("2️⃣", "Machine Learning", "Completed"),
        ("3️⃣", "Advanced ML", "Completed"),
        ("4️⃣", "Generative AI", "Completed"),
        ("5️⃣", "LLM & RAG", "In Progress"),
        ("6️⃣", "AI Agents & LangGraph", "Upcoming"),
        ("7️⃣", "Deployment & MLOps", "Upcoming"),
        ("8️⃣", "Interview & Placement Preparation", "Upcoming")
    ]

    for number, topic, status in roadmap:
        col1, col2, col3 = st.columns([1, 4, 2])

        with col1:
            st.write(number)

        with col2:
            st.write(f"**{topic}**")

        with col3:
            st.write(status)

    st.info(
        "AI-powered personalized roadmap generation will be "
        "implemented later using your resume and target job."
    )

elif page == "🎤 Interview Assistant":
    st.header("🎤 AI Interview Assistant")

    st.write(
        "Practice personalized interview questions based on "
        "your resume and target role."
    )

    col1, col2 = st.columns(2)

    with col1:
        interview_role = st.selectbox(
            "Select Interview Role",
            [
                "AI/ML Engineer",
                "Data Scientist",
                "GenAI Engineer",
                "ML Engineer"
            ]
        )

    with col2:
        interview_level = st.selectbox(
            "Select Difficulty",
            [
                "Beginner",
                "Intermediate",
                "Advanced"
            ]
        )

    st.divider()

    st.subheader("🎯 Interview Settings")

    question_type = st.multiselect(
        "Question Categories",
        [
            "Machine Learning",
            "Deep Learning",
            "Generative AI",
            "Python",
            "SQL",
            "Data Science",
            "Projects"
        ],
        default=["Machine Learning", "Projects"]
    )

    number_of_questions = st.slider(
        "Number of Questions",
        min_value=5,
        max_value=20,
        value=10
    )

    if st.button("🚀 Start Interview"):
        st.success("Interview session created!")

        st.write(
            f"**Role:** {interview_role}"
        )

        st.write(
            f"**Difficulty:** {interview_level}"
        )

        st.write(
            f"**Questions:** {number_of_questions}"
        )

        st.write(
            f"**Categories:** {', '.join(question_type)}"
        )

        st.info(
            "AI-generated questions and answer evaluation "
            "will be implemented later."
        )