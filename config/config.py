import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")