from langgraph.graph import (
    StateGraph,
    START,
    END
)

from agents.state import CareerState

from agents.profile_agent import (
    profile_analysis_agent
)

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
    interview_agent
)

from agents.report_agent import (
    report_generation_agent
)


def build_workflow():

    workflow = StateGraph(
        CareerState
    )

    workflow.add_node(
        "profile_analysis",
        profile_analysis_agent
    )

    workflow.add_node(
        "career_recommendation",
        career_recommendation_agent
    )

    workflow.add_node(
        "skill_gap",
        skill_gap_agent
    )

    workflow.add_node(
        "learning_roadmap",
        learning_roadmap_agent
    )

    workflow.add_node(
        "interview_preparation",
        interview_agent
    )

    workflow.add_node(
        "report_generation",
        report_generation_agent
    )

    workflow.add_edge(
        START,
        "profile_analysis"
    )

    workflow.add_edge(
        "profile_analysis",
        "career_recommendation"
    )

    workflow.add_edge(
        "career_recommendation",
        "skill_gap"
    )

    workflow.add_edge(
        "skill_gap",
        "learning_roadmap"
    )

    workflow.add_edge(
        "learning_roadmap",
        "interview_preparation"
    )

    workflow.add_edge(
        "interview_preparation",
        "report_generation"
    )

    workflow.add_edge(
        "report_generation",
        END
    )

    return workflow.compile()