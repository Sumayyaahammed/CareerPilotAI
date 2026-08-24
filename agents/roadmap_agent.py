from llm.llm_config import get_llm


def learning_roadmap_agent(state):

    career = state.get(
        "predicted_career",
        "Unknown"
    )

    skill_gap = state.get(
        "skill_gap",
        ""
    )

    prompt = f"""
Create a practical learning roadmap for a candidate.

Target career:
{career}

Skill gap:
{skill_gap}

Provide:

1. Beginner topics
2. Intermediate topics
3. Advanced topics
4. Projects to build
5. Recommended tools
6. Suggested certifications
7. A 3-month learning plan

Keep the recommendations realistic and structured.
"""

    llm = get_llm()

    response = llm.chat.completions.create(

        model="meta-llama/Llama-3.1-8B-Instruct",

        messages=[
            {
                "role": "system",
                "content": "You are a professional career learning advisor."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        max_tokens=800,

        temperature=0.3
    )

    roadmap = response.choices[0].message.content

    return {
        "learning_roadmap": roadmap
    }