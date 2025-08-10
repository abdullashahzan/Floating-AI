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

RULES = """
You must strictly follow these rules for every response:

1. **Format**: Always respond in valid, well-structured Markdown.
2. **Clarity**: Use plain, simple language — avoid jargon unless defining it.
3. **Structure**: Organize with headers (#, ##), subheaders, bullet points, and numbered lists where helpful.
4. **Highlighting**: Use **bold** or *italic* for emphasis on important terms.
5. **Conciseness**: Keep answers to the point — no filler or repetition.
6. **Grammar & Tone**: Use correct grammar, spelling, punctuation, and maintain a consistent, professional, and friendly tone.
7. **Readability**: Use short paragraphs and line breaks for better flow.
8. **Examples**: Provide relevant examples, definitions, or tables when useful.
9. **Voice**: Use active voice instead of passive voice.
10. **Context**: Base your response on the provided chat history and personality settings.
11. **Focus**: Only answer the user’s query — no extra commentary or unrelated information.
"""

def get_personality():
    try:
        with open("features/personality.txt", "r") as f:
            return f.read()
    except:
        return ""

def get_chat_history():
    try:
        with open("features/history.txt", "r") as f:
            return f.read()
    except:
        return ""

def get_memory():
    try:
        with open("features/memory.txt", "r") as f:
            return f.read()
    except:
        return ""

def ai_response(user_query):
    personality = get_personality()
    chat_history = get_chat_history()
    memory = get_memory()

    prompt = f"""

Information you don't need to share with user until neccessary ->
{RULES}

Personality:
{personality}

Chat History:
{chat_history}

Memory:
{memory}

User Query:
{user_query}
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an AI assistant that follows rules exactly and outputs in Markdown."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content
