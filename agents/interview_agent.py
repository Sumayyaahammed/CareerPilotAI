from llm.llm_helper import generate_response


def interview_preparation_agent(state):

    print("\n[Interview Preparation Agent]")

    profile = state.get("profile", {})
    careers = state.get("career_recommendations", [])
    skill_gap = state.get("skill_gap_analysis", "")

    prompt = f"""
You are the Interview Preparation Agent of CareerPilot AI.

Candidate profile:
{profile}

Recommended careers:
{careers}

Skill gaps:
{skill_gap}

Prepare the candidate for interviews.

Provide:

1. Technical questions
2. HR questions
3. Project-related questions
4. Python questions
5. SQL questions
6. Machine Learning questions
7. NLP/AI questions where relevant
8. Short preparation tips

Give simple and practical questions suitable for a fresher.
"""

    try:

        response = generate_response(
            prompt,
            max_tokens=1000,
            temperature=0.3
        )

        print(response)

        return {
            "interview_preparation": response
        }

    except Exception as error:

        print(
            f"Interview Preparation Agent Error: {error}"
        )

        return {
            "interview_preparation": None,
            "interview_error": str(error)
        }