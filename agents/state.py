from typing import TypedDict, Any


class CareerState(TypedDict, total=False):

    # Resume information
    resume_text: str

    education: list
    skills: list
    experience: str
    projects: list
    certifications: list

    # ML career prediction
    predicted_career: str

    # Candidate profile
    profile: dict

    # Agent outputs
    career_recommendations: list
    skill_gap_analysis: str
    learning_roadmap: str
    interview_preparation: str

    # Final output
    final_report: str

    # Error handling
    error: str

    # Optional agent error fields
    skill_gap_error: str
    roadmap_error: str
    interview_error: str
    final_report_error: str