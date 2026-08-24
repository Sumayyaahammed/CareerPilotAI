from llm.career_advisor import CareerAdvisor


def skill_gap_agent(state):

    resume_text = state.get(
        "resume_text",
        ""
    )

    predicted_career = state.get(
        "predicted_career",
        "Unknown"
    )

    context = state.get(
        "retrieved_context",
        ""
    )

    advisor = CareerAdvisor()

    profile = {
        "predicted_career": predicted_career,
        "resume": resume_text[:3000]
    }

    result = advisor.generate_skill_gap(
        profile,
        context
    )

    return {
        "skill_gap": result
    }