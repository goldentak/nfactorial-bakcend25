from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.crud import create_chat_session, get_chat_sessions, get_messages, add_message
from src.database import get_db
from src.routers.auth import get_current_user
from src.schemas import ChatRequest, ChatResponse, SessionList, MessageRead
from src.assistant.assistant import ChatAssistant

router = APIRouter(prefix="/chat", tags=["chat"])
assistant = ChatAssistant()

@router.get("/", response_model=list[SessionList])
def list_sessions(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    sessions = get_chat_sessions(db, current_user.id)
    return sessions

@router.post("/", response_model=SessionList)
def create_session(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    session = create_chat_session(db, current_user.id)
    return session

@router.get("/{session_id}/messages", response_model=list[MessageRead])
def read_messages(session_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    sessions = get_chat_sessions(db, current_user.id)
    if session_id not in [s.id for s in sessions]:
        raise HTTPException(status_code=404, detail="Session not found")
    msgs = get_messages(db, session_id)
    return msgs

@router.post("/{session_id}/message", response_model=MessageRead)
def post_message(session_id: int, req: ChatRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    sessions = get_chat_sessions(db, current_user.id)
    if session_id not in [s.id for s in sessions]:
        raise HTTPException(status_code=404, detail="Session not found")
    user_msg = add_message(db, session_id, 'user', req.message)
    reply_text = assistant.chat(req.message)
    bot_msg = add_message(db, session_id, 'bot', reply_text)
    return bot_msg
