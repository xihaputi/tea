from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import ChatRequest, ChatResponse
from ..models import ChatSession, ChatMessage, User
from ..services.llm_client import generate_chat_response

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask", response_model=ChatResponse)
def ask_chatbot(payload: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    """
    智能问答接口 (带持久化)
    AI Chatbot endpoint (with persistence)
    """
    # 1. 获取或创建会话
    if payload.session_id:
        session = db.query(ChatSession).get(payload.session_id)
        if not session:
            # 如果指定ID不存在，创建一个新的 (或者报错，这里选择创建新的容错)
            session = ChatSession(user_id=1, title=payload.question[:20]) # TODO: 关联真实用户ID
            db.add(session)
            db.commit()
            db.refresh(session)
    else:
        # 创建新会话
        # 注意: 这里暂定 user_id=1, 实际应从 token 解析当前用户
        session = ChatSession(user_id=1, title=payload.question[:20]) 
        db.add(session)
        db.commit()
        db.refresh(session)
    
    # 2. 保存用户提问
    user_msg = ChatMessage(
        session_id=session.id,
        role="user",
        content=payload.question
    )
    db.add(user_msg)
    db.commit()
    
    # 3. 生成回答 (传入 payload, 也可以传入 db 用于查找历史 context, 这里 llm_client 暂时只用 payload.history)
    # 如果希望由后端组装历史，可以在这里查询 db.query(ChatMessage).filter(session_id=...).all()
    answer = generate_chat_response(payload, db)
    
    # 4. 保存 AI 回答
    ai_msg = ChatMessage(
        session_id=session.id,
        role="assistant",
        content=answer
    )
    db.add(ai_msg)
    db.commit()
    
    return ChatResponse(answer=answer, session_id=session.id)
    return ChatResponse(answer=answer, session_id=session.id)


@router.get("/latest", response_model=dict)
def get_latest_chat_history(db: Session = Depends(get_db)):
    """
    获取最近一次聊天记录
    Get latest chat history
    """
    # 暂定 user_id=1
    user_id = 1
    
    # 查找最近的会话
    session = db.query(ChatSession).filter(ChatSession.user_id == user_id)\
        .order_by(ChatSession.created_at.desc()).first()
        
    if not session:
        return {"session_id": None, "history": []}
        
    # 获取消息
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session.id)\
        .order_by(ChatMessage.created_at.asc()).all()
        
    return {
        "session_id": session.id,
        "history": [
            {"role": msg.role, "content": msg.content, "created_at": msg.created_at} 
            for msg in messages
        ]
    }
