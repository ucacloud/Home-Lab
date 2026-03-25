import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Setup - runs once
conversation_history = []

# Loop - runs everytime I type
while True:
  user_input = input("You: ")
  if user_input == "quit":
    break

  # Add my message to history
  conversation_history.append({"role": "user", "content": user_input})

  # Send to Claude
  response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=conversation_history
  )

  # Claude's reply
  reply = response.content[0].text

  # Add Claude's reply to history
  conversation_history.append({"role": "assistant", "content": reply})

  print("Claude:", reply)