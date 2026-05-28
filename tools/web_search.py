import requests
import config

TAVILY_ENDPOINT = "https://api.tavily.com/search"

def web_search(query: str, max_results: int = 5) -> list[dict]:
    if not config.TAVILY_API_KEY:
        print("[WebSearch] TAVILY_API_KEY not set in .env")
        return []
    try:
        response = requests.post(
            TAVILY_ENDPOINT,
            json={
                "api_key": config.TAVILY_API_KEY,
                "query": query,
                "max_results": max_results,
                "search_depth": "basic",
            },
            timeout=10,
        )
        response.raise_for_status()
        results = []
        for item in response.json().get("results", []):
            results.append({
                "title":   item.get("title", "")[:80],
                "url":     item.get("url", ""),
                "snippet": item.get("content", ""),
            })
        return results
    except Exception as e:
        print(f"[WebSearch] Error: {e}")
        return []
