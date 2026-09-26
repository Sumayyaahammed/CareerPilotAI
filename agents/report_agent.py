from llm.career_advisor import CareerAdvisor


def final_report_agent(state):

    print("\n[Final Report Agent]")

    profile = state.get("profile", {})
    careers = state.get("career_recommendations", [])
    skill_gap = state.get("skill_gap", {})
    roadmap = state.get("learning_roadmap", {})
    interview = state.get("interview_preparation", {})

    advisor = CareerAdvisor()

    prompt = f"""
You are the final CareerPilot AI reporting agent.

Create a complete personalized career guidance report.

Candidate Profile:
{profile}

Career Recommendations:
{careers}

Skill Gap Analysis:
{skill_gap}

Learning Roadmap:
{roadmap}

Interview Preparation:
{interview}

Create the final report using these sections:

# CareerPilot AI Career Guidance Report

## 1. Candidate Profile

Summarize the candidate's education, skills and experience.

## 2. Career Recommendations

List all recommended careers with their match scores.

Explain why each career is suitable.

## 3. Skill Gap Analysis

Explain:
- Existing skills
- Missing skills
- Skills to improve
- Priority skills

## 4. Personalized Learning Roadmap

Provide:
- Skills to learn
- Technologies
- Projects
- Certifications
- Learning sequence
- Suggested timeline

## 5. Interview Preparation

Provide:
- Technical preparation
- HR preparation
- Project preparation
- Important interview questions

## 6. Career Action Plan

Give practical next steps for the candidate.

## 7. Final Recommendation

Give a concise conclusion.

Do not invent candidate information that is not present in the provided profile.

Use simple, professional language.
"""

    try:

        response = advisor.llm.invoke(prompt)

        if hasattr(response, "content"):
            response = response.content

        final_report = str(response)

        print("Final report generated successfully.")

        return {
            "final_report": final_report
        }

    except Exception as error:

        print("Final Report Agent Error:", error)

        return {
            "final_report":
                "Final report could not be generated. Error: "
                + str(error)
        }