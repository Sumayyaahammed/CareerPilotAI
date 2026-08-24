from llm.llm_config import get_llm

from llm.prompt_templates import (
    CAREER_ADVICE_PROMPT,
    SKILL_GAP_PROMPT,
    INTERVIEW_PROMPT
)

MODEL_ID = "meta-llama/Llama-3.1-8B-Instruct"


class CareerAdvisor:

    def __init__(self):

        self.llm = get_llm()


    def _generate(self, prompt):

        response = self.llm.chat.completions.create(

            model=MODEL_ID,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are CareerPilot AI, "
                        "a professional career guidance assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            max_tokens=700,

            temperature=0.3
        )

        return response.choices[0].message.content


    def generate_career_advice(
        self,
        profile,
        context
    ):

        prompt = CAREER_ADVICE_PROMPT.format(
            profile=profile,
            context=context
        )

        return self._generate(prompt)


    def generate_skill_gap(
        self,
        profile,
        context
    ):

        prompt = SKILL_GAP_PROMPT.format(
            profile=profile,
            context=context
        )

        return self._generate(prompt)


    def generate_interview_guidance(
        self,
        profile,
        context
    ):

        prompt = INTERVIEW_PROMPT.format(
            profile=profile,
            context=context
        )

        return self._generate(prompt)