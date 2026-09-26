from llm.llm_helper import generate_response


def learning_roadmap_agent(state):

    print("\n[Learning Roadmap Agent]")

    profile = state.get("profile", {})
    careers = state.get("career_recommendations", [])
    skill_gap = state.get("skill_gap_analysis", "")

    prompt = f"""
You are the Learning Roadmap Agent of CareerPilot AI.

Candidate profile:
{profile}

Recommended careers:
{careers}

Skill gap:
{skill_gap}

Create a personalized learning roadmap.

Include:

1. Beginner stage
2. Intermediate stage
3. Advanced stage
4. Projects to practice
5. Tools and technologies to learn
6. Suggested timeline

Make the roadmap realistic for a fresher.
"""

    try:

        response = generate_response(
            prompt,
            max_tokens=800,
            temperature=0.3
        )

        print(response)

        return {
            "learning_roadmap": response
        }

    except Exception as error:

        print(
            f"Roadmap Agent Error: {error}"
        )

        return {
            "learning_roadmap": None,
            "roadmap_error": str(error)
        }