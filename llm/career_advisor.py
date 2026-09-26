from llm.llm_config import get_llm


class CareerAdvisor:

    def __init__(self):
        self.llm = get_llm()

    def generate(self, prompt):
        """
        Generate a response using the configured LLM.
        """

        response = self.llm.chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1500,
            temperature=0.3
        )

        return response.choices[0].message.content

    def generate_career_advice(
        self,
        profile,
        context
    ):
        """
        Generate career advice using profile and RAG context.
        """

        prompt = f"""
You are CareerPilot AI, an intelligent career guidance assistant.

Candidate Profile:
{profile}

Relevant Career Knowledge:
{context}

Based on the candidate profile and the available knowledge,
provide clear and personalized career guidance.

Include:
1. Recommended careers
2. Why each career is suitable
3. Required skills
4. Skill gaps
5. Learning recommendations

Use simple and professional language.
"""

        return self.generate(prompt)