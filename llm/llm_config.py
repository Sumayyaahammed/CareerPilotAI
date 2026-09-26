import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

# ============================================================
# LLM CONFIGURATION
# ============================================================

HF_TOKEN = os.getenv("HF_TOKEN")

MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"


def get_llm():

    if not HF_TOKEN:
        raise ValueError(
            "HF_TOKEN environment variable is not set."
        )

    client = InferenceClient(
        model=MODEL_NAME,
        token=HF_TOKEN
    )

    return client