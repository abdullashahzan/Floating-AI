# Imports
from groq import Groq
from dotenv import load_dotenv
import os

# Configuring API key
load_dotenv()
api_key = os.getenv("API_TOKEN")

# Client
client = Groq(
    api_key=api_key,
)

"""
USAGE:
To get response from the AI model

from Client import ai_response
user_query = input("Enter here: ")
output = ai_response(user_query)
print(output)
"""

RULES = "These are rules you MUST make sure TO FOLLOW! 1) The output should be in Markdown."

def ai_response(user_query):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{RULES}. User query: {str(user_query)}",
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content