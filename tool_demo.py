import json
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


available_tools = {
    "search": search,
}


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


print("\n========== 1. FULL FIRST COMPLETION ==========")
print(completion.model_dump_json(indent=2))

message = completion.choices[0].message
print("first finish_reason:", completion.choices[0].finish_reason)
print("first content:", repr(message.content))


messages.append({
    "role": "assistant",
    "content": message.content,
    "tool_calls": [tool_call.model_dump() for tool_call in message.tool_calls],
})



print("\n========== 2. TOOL CALLS RETURNED BY THE MODEL ==========")
print("how many tool calls:", len(message.tool_calls))
for tool_call in message.tool_calls:
    print("id:", tool_call.id)
    print("name:", tool_call.function.name)
    print("arguments:", repr(tool_call.function.arguments), type(tool_call.function.arguments))
    print("---")


for tool_call in message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    function = available_tools[name]
    result = function(**args)

    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    })


final = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=messages,
    tools=tools,
    temperature=0,
    max_completion_tokens=1500,
)

print("final finish_reason:", final.choices[0].finish_reason)
print("answer:", final.choices[0].message.content)

print("\n--- full message history ---")
for m in messages:
    print(m)