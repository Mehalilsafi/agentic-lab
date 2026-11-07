from ddgs import DDGS


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


if __name__ == "__main__":
    print(search("history of coffee"))