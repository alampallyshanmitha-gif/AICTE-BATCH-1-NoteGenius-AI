from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def ask_question(transcript, question):

    prompt = f"""
    You are a study assistant.

    Lecture Notes:
    {transcript}

    Student Question:
    {question}

    Answer in simple language.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text