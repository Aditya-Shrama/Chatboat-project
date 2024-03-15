import google.generativeai as genai
import textwrap
from IPython.display import display
from IPython.display import Markdown
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

def TextGenerator(full_prompt):
    response = model.generate_content(full_prompt)
    print(full_prompt)
    return response.text

def get_answer(question):
    full_prompt = generate_prompt(question)
    text = TextGenerator(full_prompt)
    return text

def generate_prompt(question):
    prompt = f"User: I have a question '{question}'\n"
    prompt += f"User: answer it.\n"
    prompt += "Chatbot:"
    return prompt

def small_answer(answer):
    small_answer = TextGenerator(f"Summarize this answer ->'{answer}' only in one line maxmimum 10-15 words not more than that.")
    return small_answer

def explain_topic(topic):
    prompt = f"User: Explain this topic in details, for a student of 5th class.'\n"
    prompt += f"User:topic -> {topic}\n"
    prompt += f"User:FORMAT of reply -> title of topic....\n and then explain to work all about that topic , reader is a student.(content not more that 100words)\n"
    prompt += "Chatbot:"
    explaination = TextGenerator(prompt)
    return explaination
