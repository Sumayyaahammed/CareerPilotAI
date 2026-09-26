from llm.llm_helper import generate_response


def skill_gap_agent(state):

    print("\n[Skill Gap Agent]")

    profile = state.get("profile", {})
    careers = state.get("career_recommendations", [])

    prompt = f"""
You are the Skill Gap Agent of CareerPilot AI.

Candidate profile:
{profile}

Recommended careers:
{careers}

Identify the important skills the candidate already has
and the skills they need to improve for the recommended careers.

Return:

CURRENT SKILLS:
- ...

SKILL GAPS:
- ...

PRIORITY SKILLS:
- ...

Keep the answer practical for a fresher.
"""

    try:

        response = generate_response(
            prompt,
            max_tokens=600,
            temperature=0.3
        )

        print(response)

        return {
            "skill_gap_analysis": response
        }

    except Exception as error:

        print(
            f"Skill Gap Agent Error: {error}"
        )

        return {
            "skill_gap_analysis": None,
            "skill_gap_error": str(error)
        }