import streamlit as st

from src.utils.pdf_utils import extract_text_from_pdf
from src.utils.text_utils import clean_resume_text
from src.utils.jd_utils import process_job_description
from src.utils.skill_utils import extract_skills
from src.utils.matching_utils import compare_skills


# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="AI Career & Placement Assistant",
    page_icon="🎯",
    layout="wide",
)


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
    st.write("Your AI-powered career and placement companion.")

    resume_uploaded = bool(st.session_state.get("resume_text"))
    jd_added = bool(st.session_state.get("jd_text"))
    matched_count = len(
        st.session_state.get("last_skill_match", {}).get("matched_skills", [])
    )
    readiness = st.session_state.get("last_skill_match", {}).get(
        "match_percentage", 0
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📄 Resume", "Uploaded" if resume_uploaded else "Not Uploaded")
    col2.metric("💼 Job Description", "Added" if jd_added else "Not Added")
    col3.metric("📊 Skills Matched", matched_count)
    col4.metric("🎯 Readiness Score", f"{readiness}%")

    st.divider()
    st.subheader("🚀 What You Can Do")
    st.info(
        "Upload your resume and a job description to get skill-gap analysis, "
        "career planning, and interview preparation."
    )


# ============================================================
# RESUME ANALYSIS
# ============================================================
elif page == "📄 Resume Analysis":
    st.header("📄 Resume Analysis")
    st.write(
        "Upload your resume in PDF format. The app extracts the text and detects "
        "skills from a predefined list."
    )

    uploaded_resume = st.file_uploader(
        "Upload your Resume",
        type=["pdf"],
        help="Upload your latest resume in PDF format.",
        key="resume_pdf_uploader",
    )

    if uploaded_resume is not None:
        st.success("✅ Resume uploaded successfully!")
        st.write("**File name:**", uploaded_resume.name)
        st.write("**File size:**", f"{uploaded_resume.size / 1024:.2f} KB")

        resume_text = extract_text_from_pdf(uploaded_resume)
        cleaned_resume_text = clean_resume_text(resume_text)
        st.session_state["resume_text"] = cleaned_resume_text

        st.caption(
            f"Raw Characters: {len(resume_text)} | "
            f"Cleaned Characters: {len(cleaned_resume_text)}"
        )

        word_count = len(cleaned_resume_text.split())
        line_count = len(cleaned_resume_text.splitlines())

        detected_skills = extract_skills(cleaned_resume_text)
        st.session_state["resume_skills"] = detected_skills

        st.subheader("🛠️ Detected Skills")
        if detected_skills:
            st.success(", ".join(detected_skills))
        else:
            st.info(
                "No predefined skills detected. Check that the PDF contains "
                "selectable text and mentions supported skill keywords."
            )

        st.divider()
        st.subheader("📊 Resume Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("📝 Words", word_count)
        col2.metric("🛠️ Skills Detected", len(detected_skills))
        col3.metric("📄 Lines", line_count)

        if word_count >= 300 and len(detected_skills) >= 3:
            st.success("🟢 Resume has sufficient content for further analysis.")
        elif word_count > 0:
            st.warning("🟡 Resume uploaded, but it may need more content or skills.")
        else:
            st.error("🔴 No readable resume text was extracted.")

        if cleaned_resume_text:
            with st.expander("📄 View Extracted Resume Text"):
                st.text_area(
                    "Extracted Text",
                    cleaned_resume_text,
                    height=400,
                    key="resume_text_preview",
                )
        else:
            st.warning(
                "⚠️ No text could be extracted. This may be a scanned/image-based PDF."
            )


# ============================================================
# JOB DESCRIPTION
# ============================================================
elif page == "💼 Job Description":
    st.header("💼 Job Description")
    st.write("Paste a job description or upload it as a PDF.")

    st.subheader("📝 Paste Job Description")
    jd_text = st.text_area(
        "Paste Job Description",
        height=250,
        placeholder="Paste the complete job description here...",
        key="jd_text_input",
    )

    if st.button("🔍 Process Job Description", key="process_jd_text"):
        if jd_text.strip():
            cleaned_jd_text = process_job_description(jd_text)
            required_skills = extract_skills(cleaned_jd_text)

            st.session_state["jd_text"] = cleaned_jd_text
            st.session_state["jd_skills"] = required_skills
            st.session_state.pop("last_skill_match", None)

            st.success("✅ Job description processed successfully!")
            st.caption(f"📌 JD text stored: {len(cleaned_jd_text)} characters")

            st.subheader("🛠️ Required Skills")
            if required_skills:
                st.success(", ".join(required_skills))
            else:
                st.info("No predefined skills detected in this job description.")

            with st.expander("💼 View Processed Job Description"):
                st.text_area(
                    "Processed JD",
                    cleaned_jd_text,
                    height=300,
                    key="pasted_jd_preview",
                )
        else:
            st.warning("⚠️ Please paste a job description first.")

    st.write("**OR**")
    uploaded_jd = st.file_uploader(
        "Upload Job Description PDF",
        type=["pdf"],
        help="Upload the job description as a PDF.",
        key="jd_pdf_uploader",
    )

    if uploaded_jd is not None:
        st.success("✅ Job description PDF uploaded successfully!")
        st.write("**File name:**", uploaded_jd.name)
        st.write("**File size:**", f"{uploaded_jd.size / 1024:.2f} KB")

        jd_raw_text = extract_text_from_pdf(uploaded_jd)
        cleaned_jd_text = process_job_description(jd_raw_text)
        required_skills = extract_skills(cleaned_jd_text)

        st.session_state["jd_text"] = cleaned_jd_text
        st.session_state["jd_skills"] = required_skills
        st.session_state.pop("last_skill_match", None)

        st.subheader("🛠️ Required Skills")
        if required_skills:
            st.success(", ".join(required_skills))
        else:
            st.info("No predefined skills detected in this job description.")

        if cleaned_jd_text.strip():
            st.success("✅ JD text extracted and processed!")
            st.caption(f"📌 JD text stored: {len(cleaned_jd_text)} characters")
            with st.expander("💼 View Processed Job Description"):
                st.text_area(
                    "Processed JD",
                    cleaned_jd_text,
                    height=300,
                    key="uploaded_jd_preview",
                )
        else:
            st.warning(
                "⚠️ No text could be extracted from this PDF. "
                "It may be a scanned/image-based PDF."
            )

    if not st.session_state.get("jd_text"):
        st.info("Paste a job description or upload a PDF to continue.")


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================
elif page == "📊 Skill Gap Analysis":
    st.title("📊 Skill Gap Analysis")

    resume_skills = st.session_state.get("resume_skills", [])
    required_skills = st.session_state.get("jd_skills", [])

    if not resume_skills:
        st.warning("Please open Resume Analysis and upload/process your resume first.")
    elif not required_skills:
        st.warning(
            "Please open Job Description and process a JD containing supported skills first."
        )
    else:
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

        st.subheader("✅ Matched Skills")
        if matched:
            st.success(", ".join(matched))
        else:
            st.info("No matching skills found.")

        st.subheader("❌ Missing Skills")
        if missing:
            st.error(", ".join(missing))
        else:
            st.success("All detected required skills are matched!")

        st.caption(
            "This score measures overlap between detected keywords, not overall job suitability."
        )


# ============================================================
# CAREER ROADMAP
# ============================================================
elif page == "🗺️ Career Roadmap":
    st.header("🗺️ Personalized Career Roadmap")
    st.write(
        "Build a personalized learning path based on your current skills and career target."
    )

    st.subheader("🎯 Target Role")
    target_role = st.selectbox(
        "Select your target role",
        ["AI/ML Engineer", "Data Scientist", "GenAI Engineer", "ML Engineer"],
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
        ("8️⃣", "Interview & Placement Preparation", "Upcoming"),
    ]

    for number, topic, status in roadmap:
        col1, col2, col3 = st.columns([1, 4, 2])
        col1.write(number)
        col2.write(f"**{topic}**")
        col3.write(status)

    st.info(
        "AI-powered personalized roadmap generation will be implemented later using your resume and target job."
    )


# ============================================================
# INTERVIEW ASSISTANT
# ============================================================
elif page == "🎤 Interview Assistant":
    st.header("🎤 AI Interview Assistant")
    st.write("Practice interview questions based on your target role.")

    col1, col2 = st.columns(2)
    with col1:
        interview_role = st.selectbox(
            "Select Interview Role",
            ["AI/ML Engineer", "Data Scientist", "GenAI Engineer", "ML Engineer"],
        )
    with col2:
        interview_level = st.selectbox(
            "Select Difficulty",
            ["Beginner", "Intermediate", "Advanced"],
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
            "Projects",
        ],
        default=["Machine Learning", "Projects"],
    )
    number_of_questions = st.slider(
        "Number of Questions", min_value=5, max_value=20, value=10
    )

    if st.button("🚀 Start Interview"):
        st.success("Interview session settings saved!")
        st.write(f"**Role:** {interview_role}")
        st.write(f"**Difficulty:** {interview_level}")
        st.write(f"**Questions:** {number_of_questions}")
        st.write(f"**Categories:** {', '.join(question_type) if question_type else 'None selected'}")
        st.info("AI-generated questions and answer evaluation will be implemented later.")
