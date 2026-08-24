from llm.career_advisor import CareerAdvisor


def interview_agent(state):

    career = state.get(
        "predicted_career",
        "Unknown"
    )

    resume_text = state.get(
        "resume_text",
        ""
    )

    context = state.get(
        "retrieved_context",
        ""
    )

    advisor = CareerAdvisor()

    profile = {
        "predicted_career": career,
        "resume": resume_text[:3000]
    }

    result = advisor.generate_interview_guidance(
        profile,
        context
    )

    return {
        "interview_guidance": result
    }