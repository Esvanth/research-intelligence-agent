"""
tools/document_reader.py — Fetches and extracts clean text from URLs
"""

import requests
from bs4 import BeautifulSoup


def read_url(url: str, max_chars: int = 3000) -> dict:
    """
    Fetch a webpage and extract readable text content.

    Args:
        url:       The URL to read.
        max_chars: Maximum characters to return (keeps token usage manageable).

    Returns:
        Dict with keys: url, title, content, error (if any)
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; ResearchIntelligenceAgent/1.0)"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup  = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "Unknown Title"

        # Remove scripts, styles, navs — keep only readable content
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        paragraphs = soup.find_all("p")
        content    = " ".join(p.get_text(separator=" ").strip() for p in paragraphs)
        content    = " ".join(content.split())  # normalise whitespace

        return {
            "url":     url,
            "title":   title,
            "content": content[:max_chars],
            "error":   None,
        }

    except Exception as e:
        return {
            "url":     url,
            "title":   "",
            "content": "",
            "error":   str(e),
        }
