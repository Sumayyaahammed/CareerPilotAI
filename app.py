
import streamlit as st
import fitz
import joblib
import re
import hashlib
from pathlib import Path


# ============================================================
# CAREERPILOT AI — PRODUCTION-STYLE STREAMLIT DASHBOARD
# ============================================================

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "resume_text": "",
    "email": None,
    "phone": None,
    "education": [],
    "skills": [],
    "experience": "Not specified",
    "projects": [],
    "certifications": [],
    "predicted_career": "",
    "profile": {},
    "career_recommendations": [],
    "skill_gap_analysis": "",
    "learning_roadmap": "",
    "interview_preparation": "",
    "final_report": "",
    "resume_hash": "",
    "analysis_done": False,
    "career_error": "",
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #f7f9fc;
    }

    [data-testid="stHeader"] {
        background: rgba(247,249,252,0.92);
    }

    .hero {
        padding: 28px 32px;
        border-radius: 22px;
        background: linear-gradient(135deg, #172554 0%, #1e3a8a 55%, #2563eb 100%);
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 12px 30px rgba(30,58,138,.18);
    }

    .hero-title {
        font-size: 38px;
        font-weight: 800;
        margin: 0;
    }

    .hero-subtitle {
        font-size: 16px;
        opacity: .88;
        margin-top: 8px;
    }

    .hero-badge {
        display: inline-block;
        margin-top: 16px;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,.14);
        font-size: 13px;
    }

    .card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 14px;
        box-shadow: 0 3px 14px rgba(15,23,42,.04);
    }

    .metric {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        min-height: 108px;
        box-shadow: 0 3px 14px rgba(15,23,42,.04);
    }

    .metric-number {
        font-size: 28px;
        font-weight: 800;
        color: #172554;
    }

    .metric-label {
        color: #64748b;
        font-size: 13px;
        margin-top: 4px;
    }

    .career-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 18px;
        margin: 10px 0;
        box-shadow: 0 3px 12px rgba(15,23,42,.04);
    }

    .career-name {
        font-size: 19px;
        font-weight: 750;
        color: #0f172a;
    }

    .career-score {
        color: #2563eb;
        font-weight: 700;
        font-size: 15px;
    }

    .tag {
        display: inline-block;
        padding: 5px 10px;
        margin: 3px 4px 3px 0;
        border-radius: 999px;
        background: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #dbeafe;
        font-size: 12px;
    }

    .status {
        padding: 12px 15px;
        border-radius: 12px;
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        color: #166534;
        margin-bottom: 14px;
    }

    .muted {
        color: #64748b;
        font-size: 13px;
    }

    .section-title {
        font-size: 23px;
        font-weight: 750;
        color: #0f172a;
        margin: 5px 0 14px;
    }

    div[data-testid="stTabs"] button {
        font-weight: 650;
    }

    .disclaimer {
        padding: 13px 16px;
        border-radius: 12px;
        background: #fffbeb;
        border: 1px solid #fde68a;
        color: #78350f;
        font-size: 13px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def extract_text_from_pdf(pdf_bytes):
    document = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = []

    for page in document:
        pages.append(page.get_text())

    document.close()
    return "\n".join(pages).strip()


def clean_resume_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_email(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    matches = re.findall(pattern, text)
    return matches[0] if matches else None


def extract_phone(text):
    pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"
    matches = re.findall(pattern, text)
    return matches[0] if matches else None


def extract_education(text):
    education_keywords = [
        "B.Tech", "M.Tech", "B.E", "M.E", "B.Sc", "M.Sc",
        "BCA", "MCA", "MBA", "BBA", "PhD",
        "Bachelor of Technology", "Master of Technology",
        "Bachelor of Science", "Master of Science",
        "Computer Science and Engineering", "Computer Science",
        "Information Technology",
        "Electronics and Communication Engineering",
        "Electrical and Electronics Engineering",
        "Mechanical Engineering", "Civil Engineering",
        "Higher Secondary", "Higher Secondary Education",
        "SSLC", "ITI",
    ]

    lower_text = text.lower()
    found = [
        item for item in education_keywords
        if item.lower() in lower_text
    ]
    return list(dict.fromkeys(found))


def extract_skills(text):
    skill_database = [
        "Python", "Java", "C++", "SQL", "R Programming",
        "Machine Learning", "Deep Learning", "Data Science",
        "Artificial Intelligence", "Generative AI", "Agentic AI",
        "NLP", "Natural Language Processing", "Computer Vision",
        "Image Processing", "YOLO", "YOLOv8", "OpenCV",
        "TensorFlow", "Keras", "PyTorch", "Pandas", "NumPy",
        "Matplotlib", "Seaborn", "Scikit-learn", "RAG",
        "LangChain", "LangGraph", "FAISS", "Hugging Face",
        "Transformers", "Prompt Engineering", "MySQL", "MongoDB",
        "Flask", "FastAPI", "Streamlit", "HTML", "CSS", "JavaScript",
        "Tableau", "Power BI", "AWS", "Cloud Computing",
        "Communication", "Negotiation", "Time Management",
    ]

    lower_text = text.lower()
    found = []

    for skill in skill_database:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, lower_text):
            found.append(skill)

    return list(dict.fromkeys(found))


def extract_experience(text):
    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s+years?\s+of\s+experience",
        r"(\d+(?:\.\d+)?)\+?\s+years?\s+experience",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1) + " years"

    lower_text = text.lower()

    if "trainee" in lower_text:
        return "Trainee"
    if "intern" in lower_text:
        return "Internship experience"

    return "Not specified"


def extract_projects(text):
    project_keywords = [
        "AI-Based Workplace Mobile Usage Detection and Analysis System",
        "AI-Powered Emergency Room Patient Prioritization System",
        "Smart Farm Precision Agriculture",
        "CareerPilot AI",
    ]

    lower_text = text.lower()

    return [
        project for project in project_keywords
        if project.lower() in lower_text
    ]


def extract_certifications(text):
    certification_keywords = [
        "Cloud Computing",
        "AWS",
        "Machine Learning",
        "Data Science",
        "Python",
        "Artificial Intelligence",
    ]

    lower_text = text.lower()

    return list(dict.fromkeys([
        item for item in certification_keywords
        if item.lower() in lower_text
    ]))


@st.cache_resource
def load_models():
    model = joblib.load(MODEL_DIR / "career_classifier.pkl")
    vectorizer = joblib.load(MODEL_DIR / "tfidf_vectorizer.pkl")
    encoder = joblib.load(MODEL_DIR / "label_encoder.pkl")
    return model, vectorizer, encoder


def predict_model_career(resume_text):
    model, vectorizer, encoder = load_models()

    cleaned = clean_resume_text(resume_text)
    vectorized = vectorizer.transform([cleaned])
    prediction = model.predict(vectorized)

    return encoder.inverse_transform(prediction)[0]


def create_profile(resume_text):
    education = extract_education(resume_text)
    skills = extract_skills(resume_text)
    projects = extract_projects(resume_text)
    certifications = extract_certifications(resume_text)
    experience = extract_experience(resume_text)

    try:
        predicted = predict_model_career(resume_text)
    except Exception:
        predicted = "Not available"

    return {
        "education": education,
        "skills": skills,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
        "predicted_career": predicted,
    }


def reset_analysis():
    for key in DEFAULT_STATE:
        if key == "resume_hash":
            st.session_state[key] = ""
        elif isinstance(DEFAULT_STATE[key], list):
            st.session_state[key] = []
        elif isinstance(DEFAULT_STATE[key], dict):
            st.session_state[key] = {}
        elif isinstance(DEFAULT_STATE[key], bool):
            st.session_state[key] = False
        else:
            st.session_state[key] = DEFAULT_STATE[key]


def build_state():
    return {
        "resume_text": st.session_state["resume_text"],
        "education": st.session_state["education"],
        "skills": st.session_state["skills"],
        "experience": st.session_state["experience"],
        "projects": st.session_state["projects"],
        "certifications": st.session_state["certifications"],
        "predicted_career": st.session_state["predicted_career"],
        "profile": st.session_state["profile"],
    }


def render_tags(items):
    if not items:
        st.caption("Not detected from the uploaded resume.")
        return

    html = "".join(
        f'<span class="tag">{item}</span>'
        for item in items
    )
    st.markdown(html, unsafe_allow_html=True)


def render_agent_output(text, empty_message):
    if text:
        st.markdown(text)
    else:
        st.info(empty_message)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 🎯 CareerPilot AI")
    st.caption("Agentic Career Guidance & Skill Development")

    st.divider()

    st.markdown("### Workflow")
    st.markdown(
        """
        **1.** Resume analysis  
        **2.** Career matching  
        **3.** Skill-gap analysis  
        **4.** Learning roadmap  
        **5.** Interview preparation  
        **6.** Final career report
        """
    )

    st.divider()

    if st.session_state["analysis_done"]:
        st.success("Resume analyzed")
        st.caption(
            f"{len(st.session_state['skills'])} skills detected · "
            f"{len(st.session_state['projects'])} projects detected"
        )
    else:
        st.info("Upload a PDF resume to begin.")

    if st.button("↻ Start New Analysis", use_container_width=True):
        reset_analysis()
        st.rerun()

    st.divider()

    st.markdown("### Technology")
    st.caption(
        "Python · scikit-learn · RAG · FAISS · LLM · "
        "LangGraph · Streamlit · Agentic AI"
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🎯 CareerPilot AI</div>
        <div class="hero-subtitle">
            Personalized career guidance based on your resume, skills,
            education, projects and experience.
        </div>
        <div class="hero-badge">
            AI-assisted guidance • Resume-aware • Multi-agent workflow
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# RESUME INPUT
# ============================================================

st.markdown(
    '<div class="section-title">Start with your resume</div>',
    unsafe_allow_html=True,
)

upload_col, info_col = st.columns([1.45, 1])

with upload_col:
    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf"],
        help="Use a text-based PDF resume for the most reliable extraction.",
    )

with info_col:
    st.markdown(
        """
        <div class="card">
            <b>What CareerPilot analyzes</b><br><br>
            • Education<br>
            • Technical skills<br>
            • Experience<br>
            • Projects<br>
            • Certifications<br>
            • Career-related text from your resume
        </div>
        """,
        unsafe_allow_html=True,
    )

if uploaded_file is not None:
    pdf_bytes = uploaded_file.getvalue()
    current_hash = hashlib.md5(pdf_bytes).hexdigest()

    if current_hash != st.session_state["resume_hash"]:
        st.session_state["analysis_done"] = False
        st.session_state["resume_hash"] = current_hash

    st.caption(f"Selected file: **{uploaded_file.name}**")

    if st.button(
        "🚀 Analyze Resume",
        type="primary",
        use_container_width=True,
    ):
        reset_analysis()
        st.session_state["resume_hash"] = current_hash

        try:
            with st.status(
                "Analyzing your resume...",
                expanded=True,
            ) as status:

                st.write("📄 Extracting resume text...")
                resume_text = extract_text_from_pdf(pdf_bytes)

                if not resume_text:
                    status.update(
                        label="No readable text found",
                        state="error",
                    )
                    st.error(
                        "No text could be extracted from this PDF. "
                        "Try a text-based PDF instead of a scanned image."
                    )
                    st.stop()

                st.write("🔎 Building your resume profile...")
                profile = create_profile(resume_text)

                st.session_state["resume_text"] = resume_text
                st.session_state["email"] = extract_email(resume_text)
                st.session_state["phone"] = extract_phone(resume_text)
                st.session_state["education"] = profile["education"]
                st.session_state["skills"] = profile["skills"]
                st.session_state["experience"] = profile["experience"]
                st.session_state["projects"] = profile["projects"]
                st.session_state["certifications"] = profile["certifications"]
                st.session_state["predicted_career"] = profile["predicted_career"]
                st.session_state["profile"] = profile
                st.session_state["analysis_done"] = True

                status.update(
                    label="Resume profile created",
                    state="complete",
                )

            st.success("Resume analysis completed. You can now use the modules below.")

        except Exception as error:
            st.error(f"Resume analysis failed: {error}")


# ============================================================
# MAIN APPLICATION
# ============================================================

if not st.session_state["analysis_done"]:
    st.markdown(
        """
        <div class="disclaimer">
            <b>How it works:</b> Upload a resume and analyze it first.
            CareerPilot will then use the extracted profile as input for
            each AI guidance module. The recommendations are decision-support
            outputs, not guaranteed job outcomes.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


# ============================================================
# PROFILE OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">Resume Profile</div>',
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-number">{len(st.session_state["skills"])}</div>
            <div class="metric-label">Skills detected</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-number">{len(st.session_state["education"])}</div>
            <div class="metric-label">Education items</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-number">{len(st.session_state["projects"])}</div>
            <div class="metric-label">Projects detected</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m4:
    profile_fields = [
        bool(st.session_state["education"]),
        bool(st.session_state["skills"]),
        bool(st.session_state["experience"] != "Not specified"),
        bool(st.session_state["projects"]),
    ]
    completeness = round(sum(profile_fields) / len(profile_fields) * 100)

    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-number">{completeness}%</div>
            <div class="metric-label">Profile completeness</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with st.expander("👤 View extracted profile", expanded=False):
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Contact**")
        st.write(f"Email: {st.session_state['email'] or 'Not detected'}")
        st.write(f"Phone: {st.session_state['phone'] or 'Not detected'}")

        st.markdown("**Education**")
        if st.session_state["education"]:
            for item in st.session_state["education"]:
                st.write(f"• {item}")
        else:
            st.caption("Not detected")

        st.markdown("**Experience**")
        st.write(st.session_state["experience"])

    with c2:
        st.markdown("**Skills**")
        render_tags(st.session_state["skills"])

        st.markdown("**Projects**")
        if st.session_state["projects"]:
            for item in st.session_state["projects"]:
                st.write(f"• {item}")
        else:
            st.caption("Not detected")

        st.markdown("**Certifications / related terms**")
        render_tags(st.session_state["certifications"])

with st.expander("📄 View extracted resume text"):
    st.text_area(
        "Extracted content",
        st.session_state["resume_text"],
        height=260,
        disabled=True,
        label_visibility="collapsed",
    )


# ============================================================
# ANALYSIS MODULES
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">CareerPilot Analysis</div>',
    unsafe_allow_html=True,
)

st.caption(
    "Each module has a separate action. Results stay available while you "
    "move between sections, so expensive AI calls are not repeated unnecessarily."
)

tabs = st.tabs(
    [
        "🎯 Careers",
        "📊 Skill Gap",
        "🗺️ Roadmap",
        "💬 Interview",
        "📑 Final Report",
    ]
)


# ============================================================
# CAREER RECOMMENDATIONS
# ============================================================

with tabs[0]:
    st.markdown("### Career Recommendations")
    st.caption(
        "The AI compares your extracted profile with career patterns in "
        "the current CareerPilot knowledge base."
    )

    if st.button(
        "🎯 Generate Career Recommendations",
        key="career_button",
        type="primary",
        use_container_width=True,
    ):
        from agents.career_agent import career_recommendation_agent

        try:
            with st.spinner("Analyzing career paths..."):
                result = career_recommendation_agent(build_state())

            st.session_state["career_recommendations"] = result.get(
                "career_recommendations", []
            )
            st.session_state["career_error"] = result.get(
                "career_recommendation_error", ""
            )

            if st.session_state["career_recommendations"]:
                st.success("Career analysis completed.")
            else:
                st.warning("No career recommendations were generated.")

        except Exception as error:
            st.error(f"Career recommendation failed: {error}")

    recommendations = st.session_state["career_recommendations"]

    if recommendations:
        for index, item in enumerate(recommendations, start=1):
            career = item.get("career", "Unknown Career")
            match = item.get("match", 0)

            st.markdown(
                f"""
                <div class="career-card">
                    <div class="career-name">{index}. {career}</div>
                    <div class="career-score">AI profile match: {match}%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.progress(
                min(max(float(match) / 100, 0), 1)
            )

        st.markdown(
            """
            <div class="disclaimer">
                <b>Important:</b> A match score is an AI-generated similarity
                indicator, not a probability of employment, salary, or job success.
                Real job-market matching will become stronger when job-description
                data is added to the knowledge base.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Click the button above to generate career options.")


# ============================================================
# SKILL GAP
# ============================================================

with tabs[1]:
    st.markdown("### Skill Gap Analysis")
    st.caption(
        "Identifies skills that may need development for the recommended career paths."
    )

    if st.button(
        "📊 Generate Skill Gap Analysis",
        key="skill_button",
        type="primary",
        use_container_width=True,
    ):
        if not st.session_state["career_recommendations"]:
            st.warning("Generate Career Recommendations first.")
        else:
            from agents.skill_gap_agent import skill_gap_agent

            try:
                with st.spinner("Analyzing current skills against target careers..."):
                    state = build_state()
                    state["career_recommendations"] = st.session_state[
                        "career_recommendations"
                    ]
                    result = skill_gap_agent(state)

                st.session_state["skill_gap_analysis"] = result.get(
                    "skill_gap_analysis", ""
                )

                if st.session_state["skill_gap_analysis"]:
                    st.success("Skill gap analysis completed.")

            except Exception as error:
                st.error(f"Skill gap analysis failed: {error}")

    render_agent_output(
        st.session_state["skill_gap_analysis"],
        "Generate Career Recommendations first, then run the Skill Gap Analysis.",
    )


# ============================================================
# LEARNING ROADMAP
# ============================================================

with tabs[2]:
    st.markdown("### Personalized Learning Roadmap")
    st.caption(
        "Turns identified gaps into a practical sequence of learning topics and projects."
    )

    if st.button(
        "🗺️ Generate Learning Roadmap",
        key="roadmap_button",
        type="primary",
        use_container_width=True,
    ):
        if not st.session_state["skill_gap_analysis"]:
            st.warning("Generate Skill Gap Analysis first.")
        else:
            from agents.roadmap_agent import learning_roadmap_agent

            try:
                with st.spinner("Building your learning plan..."):
                    state = build_state()
                    state["career_recommendations"] = st.session_state[
                        "career_recommendations"
                    ]
                    state["skill_gap_analysis"] = st.session_state[
                        "skill_gap_analysis"
                    ]

                    result = learning_roadmap_agent(state)

                st.session_state["learning_roadmap"] = result.get(
                    "learning_roadmap", ""
                )

                if st.session_state["learning_roadmap"]:
                    st.success("Learning roadmap generated.")

            except Exception as error:
                st.error(f"Learning roadmap failed: {error}")

    render_agent_output(
        st.session_state["learning_roadmap"],
        "Generate Skill Gap Analysis first, then create the roadmap.",
    )


# ============================================================
# INTERVIEW PREPARATION
# ============================================================

with tabs[3]:
    st.markdown("### Interview Preparation")
    st.caption(
        "Creates interview topics and questions based on the candidate profile and career options."
    )

    if st.button(
        "💬 Generate Interview Preparation",
        key="interview_button",
        type="primary",
        use_container_width=True,
    ):
        if not st.session_state["career_recommendations"]:
            st.warning("Generate Career Recommendations first.")
        else:
            from agents.interview_agent import interview_preparation_agent

            try:
                with st.spinner("Preparing interview material..."):
                    state = build_state()
                    state["career_recommendations"] = st.session_state[
                        "career_recommendations"
                    ]

                    result = interview_preparation_agent(state)

                st.session_state["interview_preparation"] = result.get(
                    "interview_preparation", ""
                )

                if st.session_state["interview_preparation"]:
                    st.success("Interview preparation generated.")

            except Exception as error:
                st.error(f"Interview preparation failed: {error}")

    render_agent_output(
        st.session_state["interview_preparation"],
        "Generate Career Recommendations first, then prepare for interviews.",
    )


# ============================================================
# FINAL REPORT
# ============================================================

with tabs[4]:
    st.markdown("### Final Career Report")
    st.caption(
        "Combines the completed modules into one structured career-development report."
    )

    prerequisites = [
        ("Career Recommendations", st.session_state["career_recommendations"]),
        ("Skill Gap Analysis", st.session_state["skill_gap_analysis"]),
        ("Learning Roadmap", st.session_state["learning_roadmap"]),
        ("Interview Preparation", st.session_state["interview_preparation"]),
    ]

    completed = sum(bool(value) for _, value in prerequisites)

    st.progress(completed / len(prerequisites))
    st.caption(f"{completed}/4 analysis modules completed")

    if st.button(
        "📑 Generate Final Career Report",
        key="report_button",
        type="primary",
        use_container_width=True,
    ):
        missing = [name for name, value in prerequisites if not value]

        if missing:
            st.warning(
                "Complete these modules first: " + ", ".join(missing)
            )
        else:
            from agents.final_report_agent import final_report_agent

            try:
                with st.spinner("Preparing the final report..."):
                    state = {
                        "profile": st.session_state["profile"],
                        "career_recommendations": st.session_state[
                            "career_recommendations"
                        ],
                        "skill_gap_analysis": st.session_state[
                            "skill_gap_analysis"
                        ],
                        "learning_roadmap": st.session_state[
                            "learning_roadmap"
                        ],
                        "interview_preparation": st.session_state[
                            "interview_preparation"
                        ],
                    }

                    result = final_report_agent(state)

                st.session_state["final_report"] = result.get(
                    "final_report", ""
                )

                if st.session_state["final_report"]:
                    st.success("Final report generated.")

            except Exception as error:
                st.error(f"Final report failed: {error}")

    if st.session_state["final_report"]:
        st.markdown(st.session_state["final_report"])

        st.download_button(
            "⬇️ Download Career Report",
            data=st.session_state["final_report"],
            file_name="CareerPilot_Career_Report.txt",
            mime="text/plain",
            use_container_width=True,
        )
    else:
        st.info(
            "Complete the four analysis modules above before generating the final report."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="muted" style="text-align:center;">
        CareerPilot AI • Agentic Career Guidance and Skill Development Assistant<br>
        AI-generated guidance should be reviewed against current job requirements
        and the user's actual goals.
    </div>
    """,
    unsafe_allow_html=True,
)
