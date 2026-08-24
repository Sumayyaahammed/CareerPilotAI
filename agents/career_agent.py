from rag.query_engine import (
    RAGRetriever,
    build_context
)

from llm.career_advisor import CareerAdvisor


def career_recommendation_agent(state):

    resume_text = state.get(
        "resume_text",
        ""
    )

    predicted_career = state.get(
        "predicted_career",
        "Unknown"
    )

    retriever = RAGRetriever()

    query = (
        f"Career guidance for a candidate "
        f"interested in {predicted_career}. "
        f"Resume: {resume_text[:3000]}"
    )

    results = retriever.search(
        query
    )

    context = build_context(
        results
    )

    advisor = CareerAdvisor()

    profile = {
        "predicted_career": predicted_career,
        "resume": resume_text[:3000]
    }

    recommendation = advisor.generate_career_advice(
        profile,
        context
    )

    return {
        "retrieved_context": context,
        "career_recommendation": recommendation
    }