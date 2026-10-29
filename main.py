import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client=OpenAI(base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],)

completion = client.chat.completions.create(
  model="openai/gpt-oss-20b",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": " Explain how the internet works."}
  ],
  temperature=0,
  max_completion_tokens=500
  )
print(completion.choices[0].message.content)
print(completion.choices[0].finish_reason)
print(completion.usage)

