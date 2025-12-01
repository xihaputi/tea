from fastapi import APIRouter

from ..schemas import ChatRequest, ChatResponse
from ..services.llm_client import generate_chat_response

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask", response_model=ChatResponse)
def ask_chatbot(payload: ChatRequest) -> ChatResponse:
    """
    智能问答接口
    AI Chatbot endpoint
    """
    answer = generate_chat_response(payload)
    return ChatResponse(answer=answer)
