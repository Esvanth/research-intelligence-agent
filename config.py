import os
from dotenv import load_dotenv
load_dotenv()

FOUNDRY_PROJECT_ENDPOINT  = os.getenv("AZURE_AI_FOUNDRY_PROJECT_ENDPOINT", "")
MODEL_DEPLOYMENT           = os.getenv("AZURE_AI_MODEL_DEPLOYMENT", "gpt-4o")
AZURE_API_KEY              = os.getenv("AZURE_API_KEY", "")
OPENAI_API_KEY             = os.getenv("OPENAI_API_KEY", "")
TAVILY_API_KEY             = os.getenv("TAVILY_API_KEY", "")
APPINSIGHTS_CONNECTION_STR = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING", "")
MAX_SEARCH_RESULTS         = int(os.getenv("MAX_SEARCH_RESULTS", 5))
MAX_AGENT_ITERATIONS       = int(os.getenv("MAX_AGENTS_ITERATIONS", 10))
MAX_RESEARCH_ROUNDS        = int(os.getenv("MAX_RESEARCH_ROUNDS", 2))

# Derive Foundry IQ inference endpoint from the project endpoint
_base = FOUNDRY_PROJECT_ENDPOINT.split("/api/projects/")[0] if FOUNDRY_PROJECT_ENDPOINT else ""
FOUNDRY_INFERENCE_ENDPOINT = _base + "/models" if _base else ""

def validate_config():
    if not OPENAI_API_KEY and not AZURE_API_KEY:
        raise EnvironmentError("Missing API credentials: set AZURE_API_KEY or OPENAI_API_KEY in .env")
    if not FOUNDRY_INFERENCE_ENDPOINT and not OPENAI_API_KEY:
        raise EnvironmentError("Missing AZURE_AI_FOUNDRY_PROJECT_ENDPOINT in .env")
    if not TAVILY_API_KEY:
        raise EnvironmentError("Missing TAVILY_API_KEY in .env")
