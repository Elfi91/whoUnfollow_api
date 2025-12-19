# ================================
# VARIABILI
# ================================
from dotenv import load_dotenv
import os

load_dotenv()

base_url = os.getenv("BASE_URL")
github_token = os.getenv("GITHUB_TOKEN")
gemini_api_key = os.getenv("GEMINI_API_TOKEN")