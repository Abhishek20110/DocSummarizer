from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

SYSTEM_PROMPT = """
You are an enterprise-grade AI Document Summarization Engine designed for analytical, structured, and high-fidelity document synthesis.

Your task is to produce a precise, insight-dense, logically structured summary of the provided document.

----------------------------------------
OUTPUT FORMAT (STRICTLY ENFORCED)
----------------------------------------

You MUST produce output using EXACTLY the following Markdown structure:

### Overview
Write exactly 2–3 sentences that:
- Clearly state the document’s primary objective
- Summarize its core argument or function
- Indicate its scope, impact, or significance

### Key Highlights
Provide 5–8 bullet points that:
- Capture distinct, non-overlapping insights
- Follow logical progression (e.g., operational → strategic → risk)
- Use cause-effect or problem-solution framing where applicable
- Include concrete details such as metrics, technologies, constraints, trade-offs, risks, or outcomes when present

Each bullet MUST:
- Contain new, non-repetitive information
- Avoid vague phrasing
- Avoid restating the Overview
- Provide analytical depth, not surface description

----------------------------------------
QUALITY OPTIMIZATION RULES
----------------------------------------

To maximize structural sophistication and coverage quality:

- Prefer mechanism → outcome → impact structure
- Include rationale when claims are presented
- Capture implications, not just topics
- Avoid uniform sentence construction across bullets
- Avoid generic verbs (e.g., “discusses,” “highlights”) without specifics

----------------------------------------
STYLE & ACCURACY
----------------------------------------

- Tone: Professional, objective, analytical
- Use **bold formatting** for high-value entities (technologies, metrics, risks, deliverables)
- Do NOT overuse bold text
- Do NOT hallucinate
- Do NOT infer beyond the source text
- Only summarize explicitly stated information

----------------------------------------
FINAL SELF-CHECK
----------------------------------------

Verify before output:

- Overview is exactly 2–3 sentences
- Bullet count is 5–8
- No redundant bullets
- Logical flow across bullets
- Concrete detail included where available
- Headings exactly match:
  ### Overview
  ### Key Highlights

Output only the formatted summary.
"""

EVALUATION_PROMPT = """
You are a strict and detail-oriented summary evaluator.

Evaluate the summary against the original document using the following criteria:

1. Coverage (1–10)
   - Captures all major themes and consequential points
   - Includes important metrics, technologies, risks, or decisions when present

2. Faithfulness (1–10)
   - No hallucinations
   - No added claims
   - No distortion of meaning

3. Clarity & Conciseness (1–10)
   - Professional tone
   - No redundancy
   - Clear and well-structured sentences

4. Structural Sophistication (1–10)
   - Logical progression across bullets
   - Cause-effect or analytical framing
   - Non-uniform, insight-driven bullet construction
   - No simplistic listing of topics

5. Insight Density (1–10)
   - Information-dense
   - Avoids generic phrasing
   - Emphasizes implications and impact

Scoring Rules:
- 9–10: Production-grade
- 7–8: Strong but improvable
- 5–6: Surface-level
- <5: Weak summary

Return JSON only:

{
  "coverage": int,
  "faithfulness": int,
  "clarity": int,
  "structure": int,
  "insight_density": int,
  "overall": int,
  "reason": "concise explanation of weaknesses"
}
"""

async def evaluate_summary(client: AsyncOpenAI, original_text: str, summary: str):
    """Evaluates the quality of a summary using a second LLM pass."""
    try:
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": EVALUATION_PROMPT
                },
                {
                    "role": "user",
                    "content": f"ORIGINAL TEXT:\n{original_text[:10000]}\n\nSUMMARY TO EVALUATE:\n{summary}"
                }
            ],
            response_format={ "type": "json_object" },
            temperature=0.1,
            timeout=45.0
        )
        import json
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Evaluation error: {e}")
        return None

async def summarize_text(text: str):
    """Summarizes text and evaluates it using LLM-as-a-Judge."""
    if not OPENROUTER_API_KEY:
        return {"error": "OpenRouter API key not found."}

    if not text or len(text.strip()) == 0:
        return {"error": "No content to summarize."}

    # Limit text length to avoid token limits (basic truncation)
    max_chars = 15000 
    truncated_text = text[:max_chars]

    # Initialize client with OpenRouter's base URL
    client = AsyncOpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=OPENROUTER_API_KEY,
    )

    try:
        # Step 1: Generate Summary
        response = await client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                        {
                            "role": "user",
                            "content": f"""
                DOCUMENT CONTENT:
                ----------------
                {truncated_text}

                Generate the structured summary exactly as specified.
                """
                        }
                    ],
                    temperature=0.2,
                    top_p=0.9,
                    max_tokens=800,
                    timeout=90.0,
                    extra_headers={
                        "HTTP-Referer": "https://localhost:8000",
                        "X-Title": "DocSummarizer",
                    }
                )
        summary = response.choices[0].message.content.strip()

        # Step 2: Evaluate Summary (LLM-as-a-Judge)
        evaluation = await evaluate_summary(client, truncated_text, summary)

        return {
            "summary": summary,
            "evaluation": evaluation
        }
    except Exception as e:
        return {"error": f"Error during summarization: {str(e)}"}
