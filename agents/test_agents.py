from agents.workflow import build_workflow


print("=" * 60)
print("CAREERPILOT AI - AGENTIC WORKFLOW")
print("=" * 60)


workflow = build_workflow()


resume_text = """
I am a Computer Science graduate with experience in Python,
SQL, machine learning, data analysis, artificial intelligence,
and generative AI.

I have worked with Python, Pandas, NumPy, Scikit-learn,
TensorFlow, Streamlit, LangChain and RAG.

I am interested in Data Science and Artificial Intelligence.
"""


initial_state = {

    "resume_text": resume_text,

    "predicted_career": "Data Scientist",

    "profile": {},

    "retrieved_context": "",

    "career_recommendation": "",

    "skill_gap": "",

    "learning_roadmap": "",

    "interview_guidance": "",

    "final_report": ""
}


print("\nStarting agentic workflow...\n")


result = workflow.invoke(
    initial_state
)


print("=" * 60)
print("CAREERPILOT AI - FINAL REPORT")
print("=" * 60)

print(
    result.get(
        "final_report",
        "No final report generated."
    )
)


print("\n" + "=" * 60)
print("WORKFLOW COMPLETED")
print("=" * 60)