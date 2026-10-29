import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client=OpenAI(base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],)
for i in range(3):
 completion = client.chat.completions.create(
  model="openai/gpt-oss-20b",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Invent a name for a coffee shop. Reply with only the name"}
  ],
  temperature=1.8,
  )
 print(f"Run {i}: {completion.choices[0].message.content}")

