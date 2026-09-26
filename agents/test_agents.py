from agents.workflow import build_workflow


print("=" * 60)
print("CAREERPILOT AI - AGENTIC WORKFLOW")
print("=" * 60)

print("\nStarting agentic workflow...\n")


# ============================================================
# TEST PROFILE
# ============================================================

initial_state = {

    "resume_text": """
    B.Tech Computer Science and Engineering.
    Data Science and AI/ML Trainee.
    Skills include Python, SQL, Machine Learning,
    Pandas, NumPy, TensorFlow, NLP, Computer Vision,
    YOLOv8, OpenCV, RAG and Agentic AI.

    Projects include AI-Based Workplace Mobile Usage
    Detection and Analysis System, AI-Powered Emergency
    Room Patient Prioritization System and Smart Farm
    Precision Agriculture.
    """,

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
        "TensorFlow",
        "NLP",
        "Computer Vision",
        "YOLOv8",
        "OpenCV",
        "RAG",
        "Agentic AI"
    ],

    "experience": "Data Science and AI/ML Trainee",

    "projects": [
        "AI-Based Workplace Mobile Usage Detection and Analysis System",
        "AI-Powered Emergency Room Patient Prioritization System",
        "Smart Farm Precision Agriculture"
    ],

    "certifications": [
        "Cloud Computing"
    ],

    "predicted_career": "ENGINEERING",

    "profile": {}
}


# ============================================================
# BUILD WORKFLOW
# ============================================================

workflow = build_workflow()


# ============================================================
# RUN WORKFLOW
# ============================================================

result = workflow.invoke(
    initial_state
)


# ============================================================
# DISPLAY CAREER OPTIONS
# ============================================================

print("\n")
print("=" * 60)
print("MULTIPLE CAREER RECOMMENDATIONS")
print("=" * 60)


recommendations = result.get(
    "career_recommendations",
    []
)


if recommendations:

    for i, recommendation in enumerate(
        recommendations,
        start=1
    ):

        print(
            f"{i}. "
            f"{recommendation['career']} "
            f"- "
            f"{recommendation['match']}% match"
        )

else:

    print("No career recommendations generated.")


# ============================================================
# DISPLAY FINAL REPORT
# ============================================================

print("\n")
print("=" * 60)
print("CAREERPILOT AI - FINAL REPORT")
print("=" * 60)

print(
    result.get(
        "final_report",
        "Final report not generated."
    )
)
print("\n")
print("=" * 60)
print("WORKFLOW COMPLETED")
print("=" * 60)