import os
from dotenv import load_dotenv
load_dotenv()

FOUNDRY_PROJECT_ENDPOINT = os.getenv("AZURE_AI_FOUNDRY_PROJECT_ENDPOINT", "")
MODEL_DEPLOYMENT         = os.getenv("AZURE_AI_MODEL_DEPLOYMENT", "gpt-4o")
TAVILY_API_KEY           = os.getenv("TAVILY_API_KEY", "")
MAX_SEARCH_RESULTS       = int(os.getenv("MAX_SEARCH_RESULTS", 5))
MAX_AGENT_ITERATIONS     = int(os.getenv("MAX_AGENTS_ITERATIONS", 10))

def validate_config():
    if not FOUNDRY_PROJECT_ENDPOINT:
        raise EnvironmentError("Missing AZURE_AI_FOUNDRY_PROJECT_ENDPOINT in .env")
    if not TAVILY_API_KEY:
        raise EnvironmentError("Missing TAVILY_API_KEY in .env")
