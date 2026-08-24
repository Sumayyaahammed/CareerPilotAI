from rag_llm import generate_career_response


profile = {
    "education": ["B.Tech"],
    "skills": [
        "Python",
        "SQL",
        "Pandas",
        "Machine Learning"
    ],
    "experience": "Fresher",
    "predicted_career": "INFORMATION-TECHNOLOGY"
}


question = """
What career path would be suitable for this candidate
and what skills should they learn next?
"""


response = generate_career_response(
    profile,
    question
)


print("=" * 60)
print("CAREERPILOT AI RESPONSE")
print("=" * 60)

print(response)