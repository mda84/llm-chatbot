import os
from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
from datetime import datetime

# --- Rate Limiting Setup using SlowAPI ---
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="LLM Chatbot with Enhanced Features")
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

# --- Database Setup ---
from database import engine, SessionLocal, Conversation, Base
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Authentication Dependency ---
API_KEY = os.getenv("API_KEY", "secret-api-key")
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return x_api_key

# --- LLM Integration ---
# If USE_OLLAMA environment variable is "true", call Ollama API.
USE_OLLAMA = os.getenv("USE_OLLAMA", "false").lower() == "true"

if USE_OLLAMA:
    import requests
    def generate_response(user_message: str) -> str:
        url = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
        payload = {"prompt": user_message, "max_tokens": 100}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json().get("generated_text", "")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ollama API error: {e}")
else:
    from transformers import pipeline
    llm_pipeline = pipeline("text-generation", model="gpt2", max_length=100)
    def generate_response(user_message: str) -> str:
        try:
            response = llm_pipeline(user_message, num_return_sequences=1)
            return response[0]['generated_text']
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM error: {e}")

# --- Pydantic Model for Chat Messages ---
class ChatMessage(BaseModel):
    user_message: str
    session_id: Optional[str] = "default"

# --- Chat Endpoint with Logging, Authentication, and Rate Limiting ---
@app.post("/chat", dependencies=[Depends(verify_api_key), limiter.limit("5/minute")])
def chat_endpoint(message: ChatMessage, db: Session = Depends(get_db)):
    bot_response = generate_response(message.user_message)
    conv = Conversation(
        session_id=message.session_id,
        user_message=message.user_message,
        bot_response=bot_response,
        timestamp=datetime.utcnow()
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return {
        "session_id": message.session_id,
        "user_message": message.user_message,
        "bot_response": bot_response,
        "timestamp": conv.timestamp.isoformat()
    }

# --- History Endpoint to Retrieve Conversation Logs ---
@app.get("/history/{session_id}", dependencies=[Depends(verify_api_key), limiter.limit("10/minute")])
def get_history(session_id: str, db: Session = Depends(get_db)):
    conversations = db.query(Conversation).filter(Conversation.session_id == session_id).all()
    if not conversations:
        raise HTTPException(status_code=404, detail="No conversation history found.")
    return [
        {
            "user_message": conv.user_message,
            "bot_response": conv.bot_response,
            "timestamp": conv.timestamp.isoformat()
        }
        for conv in conversations
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
