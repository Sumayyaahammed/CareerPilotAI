import re
import fitz
import spacy


# Load spaCy English model
nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF resume.
    """

    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def extract_email(text):
    """
    Extract email address from resume text.
    """

    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    emails = re.findall(pattern, text)

    if emails:
        return emails[0]

    return None


def extract_phone(text):
    """
    Extract phone number from resume text.
    """

    pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"

    phones = re.findall(pattern, text)

    if phones:
        return phones[0]

    return None


def extract_education(text):
    """
    Extract common educational qualifications.
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
        "Master of Science"
    ]

    found = []

    text_lower = text.lower()

    for education in education_keywords:

        if education.lower() in text_lower:
            found.append(education)

    return list(set(found))


import pandas as pd


def load_skills(skill_file):
    """
    Load skills from CSV.
    """

    skills_df = pd.read_csv(skill_file)

    skills = (
        skills_df["skill"]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

    return skills


def extract_skills(text, skills):
    """
    Extract skills by matching the resume
    against the skills database.
    """

    found_skills = []

    text_lower = text.lower()

    for skill in skills:

        skill_lower = skill.lower()

        pattern = r"\b" + re.escape(skill_lower) + r"\b"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(set(found_skills))


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
            return match.group(1) + " years"

    return "Not specified"


#Step 12: Use spaCy for basic NLP information

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


#Step 13: Career prediction

#Now connect Module 6 to your Module 5 model.

import joblib

def predict_career(
    text,
    model_path="../models/career_classifier.pkl",
    vectorizer_path="../models/tfidf_vectorizer.pkl",
    encoder_path="../models/label_encoder.pkl"
):
    """
    Predict career category from resume text.
    """

    model = joblib.load(model_path)

    vectorizer = joblib.load(vectorizer_path)

    label_encoder = joblib.load(encoder_path)

    vectorized_text = vectorizer.transform([text])

    prediction = model.predict(vectorized_text)

    career = label_encoder.inverse_transform(prediction)

    return career[0]



def parse_resume(
    pdf_path,
    skill_file="../data/skills/skills.csv"
):
    """
    Complete resume parsing pipeline.
    """

    text = extract_text_from_pdf(pdf_path)

    skills = load_skills(skill_file)

    result = {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "education": extract_education(text),
        "skills": extract_skills(text, skills),
        "experience": extract_experience(text),
        "entities": extract_entities(text),
        "predicted_career": predict_career(text),
        "resume_text": text
    }

    return result


