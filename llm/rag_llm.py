import sys

sys.path.append("../rag")

from query_engine import (
    RAGRetriever,
    build_context
)

from career_advisor import CareerAdvisor


def generate_career_response(
    profile,
    question
):

    retriever = RAGRetriever()

    results = retriever.search(
        question,
        top_k=5
    )

    context = build_context(
        results
    )

    advisor = CareerAdvisor()

    response = advisor.generate_career_advice(
        profile,
        context
    )

    return response