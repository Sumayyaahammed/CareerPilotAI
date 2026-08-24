from typing import Dict, Any


def profile_analysis_agent(state):

    resume_text = state.get(
        "resume_text",
        ""
    )

    if not resume_text:

        return {
            "profile": {
                "summary": "No resume text provided."
            }
        }

    profile = {
        "resume_length": len(resume_text),
        "resume_preview": resume_text[:1000]
    }

    return {
        "profile": profile
    }