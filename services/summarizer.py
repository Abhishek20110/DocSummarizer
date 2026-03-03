from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def summarize_text(text: str):
    """Summarizes text using OpenRouter's model."""
    if not OPENROUTER_API_KEY:
        return "Error: OpenRouter API key not found."

    if not text or len(text.strip()) == 0:
        return "No content to summarize."

    # Limit text length to avoid token limits (basic truncation)
    max_chars = 15000 
    truncated_text = text[:max_chars]

    # Initialize client with OpenRouter's base URL
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    try:
        response = await client.chat.completions.create(
            model="nvidia/nemotron-3-nano-30b-a3b:free", 
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional document summarizer. Provide a concise summary of the following document in 5 to 10 sentences. Focus on key points and takeaways."
                },
                {
                    "role": "user",
                    "content": truncated_text
                }
            ],
            timeout=60.0,
            extra_headers={
                "HTTP-Referer": "https://localhost:8000", # Optional, for OpenRouter rankings
                "X-Title": "DocSummarizer", # Optional
            }
        )
        summary = response.choices[0].message.content
        return summary.strip()
    except Exception as e:
        return f"Error during summarization: {str(e)}"
