from rag.query_engine import (
    RAGRetriever,
    build_context
)

from llm.career_advisor import CareerAdvisor

from agents.career_recommender import recommend_careers


# ============================================================
# CAREER RECOMMENDATION AGENT
# ============================================================

def career_recommendation_agent(state):

    print("\n[Career Recommendation Agent]")

    # --------------------------------------------------------
    # Get profile information
    # --------------------------------------------------------

    profile = state.get("profile", {})

    resume_text = state.get(
        "resume_text",
        profile.get("resume_text", "")
    )

    education = state.get(
        "education",
        profile.get("education", [])
    )

    skills = state.get(
        "skills",
        profile.get("skills", [])
    )

    experience = state.get(
        "experience",
        profile.get("experience", "Not specified")
    )

    projects = state.get(
        "projects",
        profile.get("projects", [])
    )

    certifications = state.get(
        "certifications",
        profile.get("certifications", [])
    )

    predicted_career = state.get(
        "predicted_career",
        profile.get("predicted_career", "")
    )

    # --------------------------------------------------------
    # Build complete profile
    # --------------------------------------------------------

    profile["resume_text"] = resume_text
    profile["education"] = education
    profile["skills"] = skills
    profile["experience"] = experience
    profile["projects"] = projects
    profile["certifications"] = certifications
    profile["predicted_career"] = predicted_career

    # --------------------------------------------------------
    # MULTIPLE CAREER RECOMMENDATIONS
    # --------------------------------------------------------

    recommendations = recommend_careers(
        profile,
        top_n=5
    )

    print("\nRecommended careers:")

    for i, item in enumerate(
        recommendations,
        start=1
    ):

        print(
            f"{i}. "
            f"{item['career']} "
            f"- {item['match']}% match"
        )

    # --------------------------------------------------------
    # RAG RETRIEVAL
    # --------------------------------------------------------

    retriever = RAGRetriever()

    query = (
        "career opportunities and career guidance for "
        + " ".join(education)
        + " "
        + " ".join(skills)
        + " "
        + experience
    )

    rag_results = retriever.retrieve(
        query,
        top_k=5
    )

    # --------------------------------------------------------
    # Create RAG context
    # --------------------------------------------------------

    rag_context = build_context(
        rag_results
    )

    # --------------------------------------------------------
    # Update state
    # --------------------------------------------------------

    state["profile"] = profile

    state["career_recommendations"] = (
        recommendations
    )

    state["rag_context"] = rag_context

    return state