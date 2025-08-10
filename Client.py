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

RULES = "These are rules you MUST make sure TO FOLLOW! 1) The output should be in Markdown. 2) Use clear and concise language, avoiding jargon and technical terms whenever possible. 3) Organize content with headers (# Heading, ## Subheading, etc.) to create a clear structure. 4) Use bullet points and numbered lists when presenting multiple items or steps. 5) Emphasize important information using bold or italic text. 6) Keep responses concise and to the point, avoiding unnecessary information. 7) Use proper grammar, spelling, and punctuation. 8) Avoid using overly complex sentences or paragraphs. 9) Use tables or lists to compare data or present multiple items. 10) Ensure that the response is easy to read and understand, with proper line breaks and indentation. 11) Use specific examples or anecdotes to illustrate a point. 12) Provide definitions for technical terms or jargon. 13) Use active voice instead of passive voice. 14) Avoid using repetitive or redundant information. 15) Use a consistent tone and style throughout the response."

def ai_response(user_query):
    HISTORY = ""
    try:
        with open("history.txt", "r") as f:
            HISTORY = f.read()
    except:
        pass
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Rules: {RULES}. Chat history: {HISTORY}. User query: {str(user_query)}",
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content