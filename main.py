import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)
messages = [
    {"role": "system", "content": "You are a helpful research assistant."},
    {
        "role": "user",
        "content": (
            "Give me a short research brief about the history of coffee. "
            "Return it as JSON with these fields: "
            "summary (a string), key_points (a list of strings), sources (a list of URLs)."
        ),
    },
]

completion = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=messages,
    temperature=1,
    max_completion_tokens=1500,
)

text = completion.choices[0].message.content
print(repr(text))
print(completion.choices[0].finish_reason)

data = json.loads(text)
print(data["summary"])
print(data["key_points"])