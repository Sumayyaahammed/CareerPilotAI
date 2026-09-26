from agents.career_recommender import recommend_careers


profile = {

    "education": [
        "B.Tech",
        "Computer Science and Engineering"
    ],

    "skills": [
        "Python",
        "SQL",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "NLP",
        "TensorFlow",
        "YOLOv8",
        "OpenCV",
        "RAG",
        "Agentic AI"
    ],

    "experience": "Data Science and AI/ML Trainee",

    "projects": [
        "AI-Based Workplace Mobile Usage Detection",
        "AI-Powered Emergency Room Patient Prioritization System",
        "Smart Farm Precision Agriculture"
    ],

    "certifications": [
        "Cloud Computing"
    ],

    "predicted_career": "ENGINEERING",

    "resume_text": """
    B.Tech Computer Science and Engineering.
    Python SQL Machine Learning Data Science
    Artificial Intelligence Computer Vision NLP
    TensorFlow YOLOv8 OpenCV RAG Agentic AI.
    """
}


recommendations = recommend_careers(
    profile,
    top_n=5
)


print("=" * 60)
print("CAREERPILOT AI - MULTIPLE CAREER OPTIONS")
print("=" * 60)

for i, recommendation in enumerate(
    recommendations,
    start=1
):

    print(
        f"{i}. "
        f"{recommendation['career']} "
        f"- {recommendation['match']}% match"
    )