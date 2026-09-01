"""
Thin wrapper around the Gemini API so agents don't each configure their own client.
"""

import google.generativeai as genai
from app.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

_model = genai.GenerativeModel("gemini-flash-latest")


def generate(prompt: str) -> str:
    response = _model.generate_content(prompt)
    return response.text.strip()
