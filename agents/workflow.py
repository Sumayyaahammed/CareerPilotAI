from langgraph.graph import StateGraph, START, END

from agents.state import CareerState

from agents.career_agent import (
    career_recommendation_agent
)

from agents.skill_gap_agent import (
    skill_gap_agent
)

from agents.roadmap_agent import (
    learning_roadmap_agent
)

from agents.interview_agent import (
    interview_preparation_agent
)

from agents.final_report_agent import final_report_agent


def build_workflow():

    graph = StateGraph(CareerState)

    graph.add_node(
        "career_recommendation",
        career_recommendation_agent
    )

    graph.add_node(
        "skill_gap",
        skill_gap_agent
    )

    graph.add_node(
        "learning_roadmap",
        learning_roadmap_agent
    )

    graph.add_node(
        "interview_preparation",
        interview_preparation_agent
    )

    graph.add_node(
        "final_report",
        final_report_agent
    )

    graph.add_edge(
        START,
        "career_recommendation"
    )

    graph.add_edge(
        "career_recommendation",
        "skill_gap"
    )

    graph.add_edge(
        "skill_gap",
        "learning_roadmap"
    )

    graph.add_edge(
        "learning_roadmap",
        "interview_preparation"
    )

    graph.add_edge(
        "interview_preparation",
        "final_report"
    )

    graph.add_edge(
        "final_report",
        END
    )

    return graph.compile()