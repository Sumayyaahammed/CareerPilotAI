import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")


if not HF_TOKEN:
    raise ValueError(
        "HF_TOKEN not found. "
        "Please add your Hugging Face token to .env"
    )


MODEL_ID = "meta-llama/Llama-3.1-8B-Instruct"


def get_llm():

    client = InferenceClient(
        api_key=HF_TOKEN,
        provider="auto"
    )

    return client