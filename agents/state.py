from typing import TypedDict, List, Dict, Any


class CareerState(TypedDict, total=False):

    resume_text: str

    profile: Dict[str, Any]

    predicted_career: str

    retrieved_context: str

    career_recommendation: str

    skill_gap: str

    learning_roadmap: str

    interview_guidance: str

    final_report: str

    errors: List[str]