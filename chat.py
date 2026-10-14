
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAI

app = FastAPI(title="Nova AI API")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    history: list[dict] = Field(default_factory=list)


@app.get("/")
def home():
    return {
        "message": "Welcome to Nova AI!",
        "status": "online"
    }


@app.post("/api/chat")
def chat(request: ChatRequest):

    api_key = os.getenv("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")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not configured."
        )

    client = OpenAI(api_key=api_key)

    messages = [
        {
            "role": "system",
            "content": (
                "You are Nova AI, a friendly and intelligent AI assistant. "
                "You help with general questions, programming, mathematics, "
                "computer science, schoolwork, writing, and problem-solving. "
                "Explain difficult concepts in simple language. "
                "When writing code, provide clear explanations."
            )
        }
    ]

    # Include recent conversation context.
    for item in request.history[-10:]:

        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = item.get("content")

        if (
            role in ("user", "assistant")
            and isinstance(content, str)
            and len(content) <= 4000
        ):
            messages.append({
                "role": role,
                "content": content
            })

    # Add the current question.
    messages.append({
        "role": "user",
        "content": request.message.strip()
    })

    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            messages=messages,
            max_tokens=800
        )

        answer = response.choices[0].message.content

        return {
            "reply": answer or "I couldn't generate a response."
        }

    except Exception:
        # Do not expose API keys or internal service errors.
        raise HTTPException(
            status_code=502,
            detail="The AI service is temporarily unavailable."
        )

