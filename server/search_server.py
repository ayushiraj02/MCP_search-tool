# uv run server/search_server.py
# source .venv/bin/activate
# 

from typing import Any
import httpx
import os
from mcp.server.fastmcp import FastMCP

from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Load SerpAPI key from environment variable
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
print("SERPAPI_KEY:", SERPAPI_KEY)

# Initialize FastMCP server
mcp = FastMCP("search")

# SerpAPI endpoint
SERP_API_URL = "https://serpapi.com/search"

# Define the MCP tool for web search
@mcp.tool()
async def search_web(query: str) -> str:
    """Search the web using SerpAPI and return top results.

    Args:
        query: The search query string
    """
    if not SERPAPI_KEY:
        return "❌ SerpAPI key not configured."

    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": 5,  # number of results
        "engine": "google"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(SERP_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if "organic_results" not in data:
                return " No results found."

            results = data["organic_results"][:5]
            formatted_results = "\n\n".join(
                f"🔗 {r.get('title')}\n{r.get('snippet', 'No description available.')}\n{r.get('link')}"
                for r in results
            )
            return formatted_results

        except Exception as e:
            return f" Error fetching search results: {str(e)}"



if __name__ == "__main__":
    mcp.run(transport="stdio")