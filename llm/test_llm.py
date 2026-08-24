from llm_config import get_llm


print("=" * 60)
print("Testing CareerPilot AI LLM")
print("=" * 60)


client = get_llm()


response = client.chat.completions.create(

    model="meta-llama/Llama-3.1-8B-Instruct",

    messages=[
        {
            "role": "system",
            "content": (
                "You are CareerPilot AI, "
                "a helpful career guidance assistant."
            )
        },
        {
            "role": "user",
            "content": (
                "Explain what a Data Scientist does "
                "in simple terms."
            )
        }
    ],

    max_tokens=300,

    temperature=0.3
)


print("\nLLM Response:")
print(response.choices[0].message.content)