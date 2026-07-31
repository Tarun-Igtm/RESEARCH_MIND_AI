from google import genai
from dotenv import load_dotenv
import os

from utils.prompts import SUMMARY_PROMPT

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def summarize_text(text):
    """
    Generate summary using Gemini.
    """

    prompt = SUMMARY_PROMPT.format(
        paper=text
    )

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if hasattr(response, "text") and response.text:

            return response.text

        return "❌ Gemini returned an empty response."

    except Exception as e:

        return f"❌ Error while generating summary:\n\n{e}"