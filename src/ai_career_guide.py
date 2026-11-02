
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

_api_key = os.getenv("GEMINI_API_KEY")
_client = genai.Client(api_key=_api_key) if _api_key else None


def ask_career_guide(
    question,
    user_skills=None,
    target_role=None,
    chat_history=None,
):
    """Answer career questions using Gemini with conversation context."""

    if not _client:
        return "The AI Career Guide isn't configured yet. Please check the API key."

    context = f"""
You are SkillScope's AI Career Guide for students and early-career job seekers.
Give clear, practical, supportive, honest career advice.
Explain technical concepts in beginner-friendly language.
Use earlier messages to understand follow-up questions.
Do not guarantee employment or invent job-market facts.

User skills: {user_skills or "Not provided"}
Target role: {target_role or "Not specified"}
"""

    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=context)],
        )
    ]

    for message in (chat_history or []):
        role = message.get("role")
        text = message.get("content", "")

        if role in ("user", "model") and text:
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=text)],
                )
            )

    contents.append(
        types.Content(
            role="user",
            parts=[types.Part(text=question)],
        )
    )

    for attempt in range(3):
        try:
            response = _client.models.generate_content(
                model="gemini-3.6-flash",
                contents=contents,
            )
            return response.text or "I couldn't generate a response. Please try again."

        except Exception as e:
            error = str(e)
            print(f"Gemini API error: {error}")

            if "503" in error and attempt < 2:
                time.sleep(2 ** (attempt + 1))
                continue

            return (
                "The AI Career Guide is temporarily unavailable. "
                "Please try again in a moment."
            )