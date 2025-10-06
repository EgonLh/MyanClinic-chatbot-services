from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_service import rag_chat

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

@router.post("/ask", response_model=ChatResponse)
async def ask_chatbot(request: ChatRequest):
    try:
        answer = rag_chat(request.query)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
