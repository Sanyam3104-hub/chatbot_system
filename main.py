from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import requests
import os

app = FastAPI()

# Allow Streamlit to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


@app.post("/chat")
async def chat(request: Request):
    # DEBUG: log raw body
    raw_body = await request.body()
    print(f"Raw incoming body: {raw_body}")

    try:
        body = await request.json()
    except Exception as e:
        return JSONResponse(content={"error": f"Invalid JSON: {str(e)}"}, status_code=400)

    messages = body.get("messages")
    if not messages:
        return JSONResponse(content={"error": "No 'messages' field provided"}, status_code=400)

    # Call Groq API (non-streaming for simplicity)
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": messages,
        "stream": False
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        data = response.json()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
