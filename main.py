import os
import time
import base64
import logging
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

import google.generativeai as genai
from google.api_core.exceptions import PermissionDenied, GoogleAPIError

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

app = FastAPI()

SYSTEM_INSTRUCTION = """You are a friendly, expert assistant specialized ONLY in movies and anime.
Answer all general domain questions such as recommendations, watch orders, content warnings, and streaming availability guidance.
Add disclaimers only where genuinely needed.
Politely refuse and redirect any requests that are off-topic (e.g. homework, politics, video games, music).
Refuse serious diagnoses/medical advice, prescription-level instructions, content that facilitates harm.
Refuse piracy assistance or illegal streaming links.
Be spoiler-free by default. Offer spoiler details only when the user explicitly asks."""

class HistoryItem(BaseModel):
    role: str
    parts: List[str]

class ChatRequest(BaseModel):
    message: str
    history: List[HistoryItem] = []

def call_gemini_with_retry(fn):
    try:
        return fn()
    except Exception as e:
        status = getattr(e, 'code', None) or getattr(getattr(e, 'response', None), 'status_code', None)
        if status == 429:
            time.sleep(2)
            try:
                return fn()
            except Exception:
                return {"reply": "I'm a bit busy right now — please try again in a moment."}
        if isinstance(e, (PermissionDenied, GoogleAPIError)) or status == 403:
            return {"reply": f"API error: {str(e)}"}
        
        logging.exception("Gemini call failed")
        return {"reply": "Something went wrong — please retry."}

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    with open("code.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/chat")
async def chat(request: ChatRequest):
    def make_call():
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
            system_instruction=SYSTEM_INSTRUCTION
        )
        
        # Convert history format
        formatted_history = []
        for item in request.history:
            formatted_history.append({
                "role": "model" if item.role == "model" else "user",
                "parts": [{"text": p} for p in item.parts]
            })
            
        chat_session = model.start_chat(history=formatted_history)
        response = chat_session.send_message(request.message)
        return {"reply": response.text}
        
    return call_gemini_with_retry(make_call)

@app.post("/vision")
async def vision(file: UploadFile = File(...), message: Optional[str] = Form(None)):
    def make_call():
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
            system_instruction=SYSTEM_INSTRUCTION + "\n\nIf the provided image is NOT movie or anime related, you MUST politely refuse and redirect."
        )
        
        # Read the file synchronously for the retry block to work without issues
        file_bytes = file.file.read()
        file.file.seek(0) # reset pointer in case of retry
        
        contents = [
            {
                "mime_type": file.content_type,
                "data": base64.b64encode(file_bytes).decode("utf-8")
            }
        ]
        if message:
            contents.append(message)
            
        response = model.generate_content(contents)
        return {"reply": response.text}
        
    return call_gemini_with_retry(make_call)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
