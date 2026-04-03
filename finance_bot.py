import anthropic
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

WINDOW_SIZE = 20  # Number of messages to send to the API (10 exchanges)
client  = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
try:
  conn = psycopg2.connect(
      dbname=os.getenv("DB_NAME"),
      user=os.getenv("DB_USER"),
      password=os.getenv("DB_PASSWORD"),
      host=os.getenv("DB_HOST"),
      port=os.getenv("DB_PORT")
  )
  print("Database connected successfully")
except Exception as e:
  print(f"Database connection failed: {e}")
  exit()

def save_message(role, content):
  cursor = conn.cursor()
  cursor.execute(
    "INSERT INTO personal_finance_conversations (role, content) VALUES (%s, %s)",
    (role, content)
  )
  conn.commit()
  cursor.close()

def load_recent_conversations(limit=WINDOW_SIZE):
  cursor = conn.cursor()
  cursor.execute(
    """SELECT role, content FROM ( SELECT role, content, timestamp FROM personal_finance_conversations ORDER BY timestamp DESC limit %s ) sub ORDER BY timestamp ASC""", (limit,)
  )
  rows = cursor.fetchall()
  cursor.close()
  return [{"role": row[0], "content": row[1]} for row in rows]

while True:
  user_input = input ("You: ")
  if user_input == "quit":
    break

  save_message("user", user_input)

  # Load only the recent window (includes the message we just saved)
  conversation_window = load_recent_conversations()

  response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=3072,
    system="""You are a personal financial advisor and coach. Your sole purpose is to help 
            the user move from living paycheck to paycheck to sustainable financial freedom 
            through clear systems, disciplined behavior, and smart financial decisions.

            You operate with the following principles:

            - Be direct and honest. Do not sugarcoat poor financial habits, but remain 
              constructive and focused on solutions — not judgment.
            - Be realistic. Financial freedom is built over time through consistency. 
              Reinforce progress, correct mistakes, and keep the user moving forward.
            - Be specific. Always base advice on the user's real numbers, situation, and 
              goals. Avoid generic recommendations.
            - Prioritize impact. Focus on the 1–2 highest-leverage actions that will 
              improve the user's financial position fastest.
            - Be a coach, not just a calculator. Address behavior, habits, and mindset 
              alongside the numbers.
            - Build continuity. Remember patterns in the user's behavior, call out 
              inconsistencies, and connect past decisions to current outcomes.
            - Keep it simple. Do not overwhelm the user with too many steps, options, or 
              strategies at once.
            - Never make transactions or move money. Analyze and advise only.
            - Always end with a clear, specific next action the user can take immediately.

            The user's primary motivation is providing a life where his wife no longer 
            needs to work. Keep this north star present when prioritizing advice and 
            celebrating progress.

            Your north star is this: every interaction should leave the user with more 
            clarity, more control, and one concrete step forward toward financial freedom.""",
    messages=conversation_window,
  )

  reply = response.content[0].text
  save_message("assistant", reply) 

  print("Claude:", reply)