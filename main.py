import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError

from models import Brief

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
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "brief",
            "strict": True,
            "schema": Brief.model_json_schema(),
        },
    },
)
print(json.dumps(Brief.model_json_schema(), indent=2))

text = completion.choices[0].message.content
print(repr(text))
print(completion.choices[0].finish_reason)

try:
    brief = Brief.model_validate_json(text)
    print(brief.summary)
    for point in brief.key_points:
        print("-", point)
except ValidationError as e:
    print("Output didn't match the Brief shape:")
    print(e)