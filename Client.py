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

AVAILABLE_MODELS = ['meta-llama/llama-4-scout-17b-16e-instruct','meta-llama/llama-guard-4-12b','meta-llama/llama-prompt-guard-2-22m','meta-llama/llama-prompt-guard-2-86m','moonshotai/kimi-k2-instruct']

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
10. **Context**: Base your response on the provided chat history, your in-build persistant memory and personality settings.
11. **Focus**: Only answer the user’s query — no extra commentary or unrelated information.
"""

def get_personality():
    try:
        with open("features/personality.txt", "r") as f:
            return f.read()
    except:
        return ""

def get_memory(maxchars=10000):
    try:
        with open("features/memory.txt", "r") as f:
            memory = f.read()
        return memory[-maxchars:]
    except:
        return ""

def ai_response(user_query):
    personality = get_personality()
    memory = get_memory()

    prompt = f"""
{RULES}

Your Personality:
{personality}

Your Memory:
{memory}

User Query:
{user_query}
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an AI assistant that follows rules exactly and outputs in Markdown."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7,
        model=AVAILABLE_MODELS[0],
    )
    return chat_completion.choices[0].message.content.strip()