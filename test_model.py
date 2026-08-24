import joblib
import re


MODEL_PATH = "models/career_classifier.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"
ENCODER_PATH = "models/label_encoder.pkl"


model = joblib.load(
    MODEL_PATH
)

vectorizer = joblib.load(
    VECTORIZER_PATH
)

encoder = joblib.load(
    ENCODER_PATH
)


resume_text = """
B.Tech Computer Science graduate.
Skills include Python, SQL, Pandas, NumPy,
Machine Learning, Scikit-learn, TensorFlow,
Data Analysis and Streamlit.
Worked on machine learning and data science projects.
"""


def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"http\S+|www\S+",
        " ",
        text
    )

    text = re.sub(
        r"\S+@\S+",
        " ",
        text
    )

    text = re.sub(
        r"\d+",
        " ",
        text
    )

    text = re.sub(
        r"[^a-zA-Z\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


cleaned_text = clean_text(
    resume_text
)


features = vectorizer.transform(
    [cleaned_text]
)


prediction = model.predict(
    features
)


career = encoder.inverse_transform(
    prediction
)


print("=" * 60)
print("CAREERPILOT AI - MODEL TEST")
print("=" * 60)

print()

print(
    "Predicted Career:",
    career[0]
)

print()

print("=" * 60)