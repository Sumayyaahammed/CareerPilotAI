from llm.llm_config import get_llm


def report_generation_agent(state):

    career = state.get(
        "predicted_career",
        "Unknown"
    )

    recommendation = state.get(
        "career_recommendation",
        ""
    )

    skill_gap = state.get(
        "skill_gap",
        ""
    )

    roadmap = state.get(
        "learning_roadmap",
        ""
    )

    interview = state.get(
        "interview_guidance",
        ""
    )

    prompt = f"""
Create a final CareerPilot AI career guidance report.

Predicted Career:
{career}

Career Recommendation:
{recommendation}

Skill Gap:
{skill_gap}

Learning Roadmap:
{roadmap}

Interview Guidance:
{interview}

Structure the final report as:

1. Candidate Career Profile
2. Recommended Career
3. Why This Career
4. Skill Gap
5. Learning Roadmap
6. Interview Preparation
7. Final Recommendations

Use clear and professional language.
"""

    llm = get_llm()

    response = llm.chat.completions.create(

        model="meta-llama/Llama-3.1-8B-Instruct",

        messages=[
            {
                "role": "system",
                "content": "You are a professional career guidance report writer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        max_tokens=1200,

        temperature=0.3
    )

    report = response.choices[0].message.content

    return {
        "final_report": report
    }