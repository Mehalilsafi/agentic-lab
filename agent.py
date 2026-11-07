import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import AVAILABLE_TOOLS, TOOLS

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)

MODEL = "openai/gpt-oss-20b"

messages = [
    {
        "role": "system",
        "content": (
            "You are a research assistant. Use search to find relevant pages, "
            "then fetch_page to read the most promising ones before answering. "
            "Cite the URLs you actually read."
        ),
    },
    {"role": "user", "content": "When and where was coffee first cultivated?"},
]


completion = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=TOOLS,
    temperature=0,
    max_completion_tokens=2000,
)
message = completion.choices[0].message
print("call 1 finish_reason:", completion.choices[0].finish_reason)
print("call 1 prompt_tokens:", completion.usage.prompt_tokens)

messages.append({
    "role": "assistant",
    "content": message.content,
    "tool_calls": [tool_call.model_dump() for tool_call in message.tool_calls],
})


for tool_call in message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print(f"\n>>> model asked for: {name}({args})")

    if name not in AVAILABLE_TOOLS:
        result = f"Error: there is no tool named '{name}'. Available tools: {list(AVAILABLE_TOOLS)}"
    else:
        result = AVAILABLE_TOOLS[name](**args)
    print(f"    result: {len(result)} characters")

    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    })

# Call 2: the model reads the results.
completion = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=TOOLS,
    temperature=0,
    max_completion_tokens=2000,
)
message = completion.choices[0].message
print("\ncall 2 finish_reason:", completion.choices[0].finish_reason)
print("call 2 prompt_tokens:", completion.usage.prompt_tokens)
print("call 2 content:", message.content)

if message.tool_calls:
    print("\nThe model wants MORE tools, but this script stops here:")
    for tool_call in message.tool_calls:
        print(f"    {tool_call.function.name}({tool_call.function.arguments})")