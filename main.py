import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "My name is Safi."},
]

# Call 1
completion = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=messages,
    temperature=0,
    max_completion_tokens=500,
)
reply_text = completion.choices[0].message.content
print("Call 1:", reply_text)
print("Call 1 usage:", completion.usage.prompt_tokens, "prompt tokens")

# Save the model's reply, then add the next question
messages.append({"role": "assistant", "content": reply_text})
messages.append({"role": "user", "content": "What is my name?"})

# Call 2: send the WHOLE history again
completion = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=messages,
    temperature=0,
    max_completion_tokens=500,
)
print("Call 2:", completion.choices[0].message.content)
print("Call 2 usage:", completion.usage.prompt_tokens, "prompt tokens")
print(completion.choices[0].finish_reason)

print(messages)
