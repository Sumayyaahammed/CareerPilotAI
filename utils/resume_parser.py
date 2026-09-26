import re
from pathlib import Path

import fitz
import spacy
import pandas as pd
import joblib

# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"

SKILL_FILE = DATA_DIR / "skills" / "skills.csv"

MODEL_FILE = MODEL_DIR / "career_classifier.pkl"
VECTORIZER_FILE = MODEL_DIR / "tfidf_vectorizer.pkl"
ENCODER_FILE = MODEL_DIR / "label_encoder.pkl"


# ============================================================
# LOAD SPACY MODEL
# ============================================================

nlp = spacy.load("en_core_web_sm")


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF resume.
    """

    document = fitz.open(str(pdf_path))

    text = ""

    for page in document:
        text += page.get_text()
        text += "\n"

    document.close()

    return text


# ============================================================
# EMAIL EXTRACTION
# ============================================================

def extract_email(text):
    """
    Extract email address from resume text.
    """

    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    emails = re.findall(
        pattern,
        text
    )

    if emails:
        return emails[0]

    return None


# ============================================================
# PHONE EXTRACTION
# ============================================================

def extract_phone(text):
    """
    Extract Indian phone number from resume text.
    """

    pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"

    phones = re.findall(
        pattern,
        text
    )

    if phones:
        return phones[0]

    return None


# ============================================================
# EDUCATION EXTRACTION
# ============================================================
def extract_education(text):
    """
    Extract educational qualifications from resume text.
    """

    education_keywords = [
        "B.Tech",
        "M.Tech",
        "B.E",
        "M.E",
        "B.Sc",
        "M.Sc",
        "BCA",
        "MCA",
        "MBA",
        "BBA",
        "PhD",
        "Bachelor of Technology",
        "Master of Technology",
        "Bachelor of Science",
        "Master of Science",
        "PLUS TWO",
        "PLUS 2",
        "12TH",
        "HIGHER SECONDARY EDUCATION",
        "SSLC",
        "10TH",
        "SECONDARY SCHOOL",
        "ITI",
        "DIPLOMA",
        "VOCATIONAL",
        "COMPUTER EDUCATION",
        "DIESEL MECHANIC"
    ]

    found = []

    text_lower = text.lower()

    for education in education_keywords:

        if education.lower() in text_lower:

            found.append(education)

    return sorted(set(found))


# ============================================================
# LOAD SKILLS
# ============================================================

def load_skills(skill_file=SKILL_FILE):
    """
    Load skills from CSV.
    """

    skills_df = pd.read_csv(
        skill_file
    )

    skills = (

        skills_df["skill"]

        .dropna()

        .astype(str)

        .str.strip()

        .tolist()

    )

    return skills


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(text, skills):
    """
    Extract skills by matching the resume
    against the skills database.
    """

    found_skills = []

    text_lower = text.lower()

    for skill in skills:

        skill_lower = skill.lower()

        pattern = (
            r"\b"
            + re.escape(skill_lower)
            + r"\b"
        )

        if re.search(
            pattern,
            text_lower
        ):

            found_skills.append(
                skill
            )

    return sorted(
        set(found_skills)
    )


# ============================================================
# EXPERIENCE EXTRACTION
# ============================================================

def extract_experience(text):
    """
    Extract approximate years of experience.
    """

    patterns = [

        r"(\d+(?:\.\d+)?)\+?\s+years?\s+of\s+experience",

        r"(\d+(?:\.\d+)?)\+?\s+years?\s+experience"

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return (
                match.group(1)
                + " years"
            )

    return "Not specified"


# ============================================================
# SPACY NAMED ENTITIES
# ============================================================

def extract_entities(text):
    """
    Extract named entities using spaCy.
    """

    doc = nlp(text)

    entities = []

    for ent in doc.ents:

        entities.append({

            "text": ent.text,

            "label": ent.label_

        })

    return entities


# ============================================================
# CAREER PREDICTION
# ============================================================

def predict_career(
    text,
    model_path=None,
    vectorizer_path=None,
    encoder_path=None
):

    if model_path is None:
        model_path = MODEL_DIR / "career_classifier.pkl"

    if vectorizer_path is None:
        vectorizer_path = MODEL_DIR / "tfidf_vectorizer.pkl"

    if encoder_path is None:
        encoder_path = MODEL_DIR / "label_encoder.pkl"

    model = joblib.load(model_path)

    vectorizer = joblib.load(
        vectorizer_path
    )

    label_encoder = joblib.load(
        encoder_path
    )

    vectorized_text = vectorizer.transform(
        [text]
    )

    prediction = model.predict(
        vectorized_text
    )

    career = label_encoder.inverse_transform(
        prediction
    )

    return career[0]


# ============================================================
# COMPLETE RESUME PARSER
# ============================================================

def parse_resume(
    pdf_path,
    skill_file=None
):

    if skill_file is None:
        skill_file = SKILL_FILE

    text = extract_text_from_pdf(
        pdf_path
    )

    skills = load_skills(
        skill_file
    )

    result = {

        "email": extract_email(text),

        "phone": extract_phone(text),

        "education": extract_education(text),

        "skills": extract_skills(
            text,
            skills
        ),

        "experience": extract_experience(
            text
        ),

        "entities": extract_entities(
            text
        ),

        "predicted_career": predict_career(
            text
        ),

        "resume_text": text
    }

    return result