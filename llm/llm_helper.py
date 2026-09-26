from llm.llm_config import get_llm


def generate_response(
    prompt,
    max_tokens=1500,
    temperature=0.3
):
    llm = get_llm()

    response = llm.chat_completion(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )

    return response.choices[0].message.content