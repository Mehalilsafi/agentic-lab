import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)


def search(query: str) -> str:
    print(">>> search() WAS CALLED with:", query)
    return "Coffee was first cultivated in Yemen in the 15th century. (source: https://example.com/coffee)"


# 2. The tool schema: the DESCRIPTION of the function that we send to the model.
tools = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search the web for information about a topic. Returns a short text result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query, e.g. 'history of coffee'",
                    },
                },
                "required": ["query"],
            },
        },
    }
]

messages = [
    {"role": "system", "content": "You are a research assistant. Use the search tool to find facts."},
    {"role": "user", "content": "When was coffee first cultivated?"},
]

completion = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=messages,
    tools=tools,
    temperature=0,
    max_completion_tokens=1500,
)

message = completion.choices[0].message
print("finish_reason:", completion.choices[0].finish_reason)
print("content:", repr(message.content))
print(message.model_dump_json(indent=2))