import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

MAX_PAGE_CHARS = 8000
HEADERS = {"User-Agent": "research-agent/0.1 (learning project)"}


def search(query: str) -> str:
    try:
        results = DDGS().text(query, max_results=5)
    except Exception as e:
        return f"Error: search failed: {e}"

    if not results:
        return "No results found."

    lines = []
    for r in results:
        lines.append(f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}")
    return "\n\n".join(lines)


def fetch_page(url: str) -> str:
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Error: could not fetch {url}: {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)

    if len(text) > MAX_PAGE_CHARS:
        text = text[:MAX_PAGE_CHARS] + "\n\n[...page truncated...]"
    return text


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": (
                "Search the web. Returns up to 5 results, each with a title, URL, and short snippet. "
                "Snippets are brief and may be incomplete: to read a page's actual content, "
                "call fetch_page with its URL. Use short, specific queries."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A short, specific search query, e.g. 'coffee origin Ethiopia Yemen'",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_page",
            "description": (
                "Download a web page and return its readable text, truncated to about 8000 characters. "
                "Use this on the most promising URLs from search results to read the real content "
                "before answering. Only pass full URLs starting with http:// or https://."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The full URL of the page to read, copied from a search result.",
                    },
                },
                "required": ["url"],
            },
        },
    },
]

AVAILABLE_TOOLS = {
    "search": search,
    "fetch_page": fetch_page,
}


if __name__ == "__main__":
    print(search("history of coffee"))
    print("=" * 40)
    page = fetch_page("https://en.wikipedia.org/wiki/History_of_coffee")
    print(len(page), "characters")
    print(page[:1000])