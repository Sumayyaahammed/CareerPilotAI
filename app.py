import streamlit as st
import fitz
import joblib
import re
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR / "models"


# ============================================================
# LOAD TRAINED MODELS
# ============================================================

@st.cache_resource
def load_models():

    model = joblib.load(
        MODEL_DIR / "career_classifier.pkl"
    )

    vectorizer = joblib.load(
        MODEL_DIR / "tfidf_vectorizer.pkl"
    )

    label_encoder = joblib.load(
        MODEL_DIR / "label_encoder.pkl"
    )

    return model, vectorizer, label_encoder


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_resume_text(text):

    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(
        r"http\S+|www\S+",
        " ",
        text
    )

    # Remove emails
    text = re.sub(
        r"\S+@\S+",
        " ",
        text
    )

    # Remove numbers
    text = re.sub(
        r"\d+",
        " ",
        text
    )

    # Remove special characters
    text = re.sub(
        r"[^a-zA-Z\s]",
        " ",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# CAREER PREDICTION
# ============================================================

def predict_career(resume_text):

    model, vectorizer, label_encoder = load_models()

    # Clean resume
    cleaned_text = clean_resume_text(
        resume_text
    )

    # Convert text into TF-IDF
    vectorized_text = vectorizer.transform(
        [cleaned_text]
    )

    # Predict encoded class
    prediction = model.predict(
        vectorized_text
    )

    # Convert encoded class to career name
    career = label_encoder.inverse_transform(
        prediction
    )

    return career[0]


# ============================================================
# HEADER
# ============================================================

st.title("🎯 CareerPilot AI")

st.subheader(
    "Agentic AI Career Guidance and Skill Development Assistant"
)

st.write(
    """
    Upload your resume and CareerPilot AI will analyze your
    profile and provide personalized career guidance.
    """
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("CareerPilot AI")

    st.write(
        """
        This system uses:

        • Machine Learning
        • NLP
        • RAG
        • LLM
        • LangGraph
        • Agentic AI
        """
    )

    st.divider()

    st.info(
        "Upload a PDF resume to begin."
    )


# ============================================================
# RESUME UPLOAD
# ============================================================

st.header("📄 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose your resume PDF",
    type=["pdf"]
)


# ============================================================
# PDF PROCESSING
# ============================================================

if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button(
        "🚀 Analyze Resume",
        type="primary"
    ):

        # ----------------------------------------------------
        # EXTRACT TEXT
        # ----------------------------------------------------

        try:

            pdf_bytes = uploaded_file.getvalue()

            document = fitz.open(
                stream=pdf_bytes,
                filetype="pdf"
            )

            resume_text = ""

            for page in document:

                resume_text += page.get_text()

                resume_text += "\n"

            document.close()

            resume_text = resume_text.strip()


            if not resume_text:

                st.error(
                    "No text could be extracted from this PDF."
                )

                st.stop()


            st.success(
                "Resume text extracted successfully!"
            )


        except Exception as error:

            st.error(
                f"PDF extraction failed: {error}"
            )

            st.stop()


        # ----------------------------------------------------
        # SHOW RESUME TEXT
        # ----------------------------------------------------

        with st.expander(
            "📋 View Extracted Resume Text"
        ):

            st.text_area(
                "Resume Content",
                resume_text,
                height=350
            )


        # ----------------------------------------------------
        # CAREER PREDICTION
        # ----------------------------------------------------

        with st.spinner(
            "🤖 Predicting your career..."
        ):

            try:

                predicted_career = predict_career(
                    resume_text
                )

            except Exception as error:

                st.error(
                    f"Career prediction failed: {error}"
                )

                st.stop()


        # ----------------------------------------------------
        # DISPLAY CAREER
        # ----------------------------------------------------

        st.divider()

        st.header(
            "🎯 Career Prediction"
        )

        st.success(
            f"Recommended Career Category: **{predicted_career}**"
        )


        # ----------------------------------------------------
        # STORE DATA
        # ----------------------------------------------------

        st.session_state[
            "resume_text"
        ] = resume_text

        st.session_state[
            "predicted_career"
        ] = predicted_career


else:

    st.info(
        "Please upload your resume PDF to begin."
    )