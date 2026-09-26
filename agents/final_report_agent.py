from llm.llm_helper import generate_response


def final_report_agent(state):

    print("\n[Final Report Agent]")

    profile = state.get("profile", {})
    careers = state.get("career_recommendations", [])
    skill_gap = state.get("skill_gap_analysis", "")
    roadmap = state.get("learning_roadmap", "")
    interview = state.get("interview_preparation", "")

    prompt = f"""
You are the Final Report Agent of CareerPilot AI.

Create a final career guidance report using the information provided below.

CANDIDATE PROFILE:
{profile}

CAREER RECOMMENDATIONS:
{careers}

SKILL GAP ANALYSIS:
{skill_gap}

LEARNING ROADMAP:
{roadmap}

INTERVIEW PREPARATION:
{interview}

Create the report using exactly these sections:

## 1. Candidate Profile

Summarize the candidate's education, skills, experience, and relevant background.

## 2. Career Recommendations

List all recommended careers with their match scores.

## 3. Why These Careers

Explain why each recommended career is suitable based only on the candidate profile and available analysis.

## 4. Skill Gap Analysis

Clearly mention:
- Current skills
- Missing skills
- Priority skills to improve

## 5. Personalized Learning Roadmap

Give a practical roadmap divided into stages.

## 6. Interview Preparation

Provide:
- Technical preparation
- HR preparation
- Project preparation
- Important topics to revise

## 7. Final Recommendations

Give clear next steps for the candidate.

IMPORTANT:
- Do not invent candidate information.
- Use only the information provided above.
- Keep the report professional and easy to understand.
- Do not repeat the same information unnecessarily.
- Make the report useful for a fresher or entry-level candidate.
"""

    try:

        response = generate_response(
            prompt,
            max_tokens=1800,
            temperature=0.3
        )

        print("Final report generated successfully.")

        return {
            "final_report": response
        }

    except Exception as error:

        print(f"Final Report Agent Error: {error}")

        return {
            "final_report": None,
            "final_report_error": str(error)
        }