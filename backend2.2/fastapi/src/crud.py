from sqlalchemy.orm import Session
from .models import User, ChatSession, ChatMessage, FetchLog
from .schemas import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User CRUD

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    hashed = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if user and pwd_context.verify(password, user.hashed_password):
        return user
    return None


def change_username(db: Session, user: User, new_username: str):
    user.username = new_username
    db.commit()


def change_password(db: Session, user: User, new_password: str):
    user.hashed_password = pwd_context.hash(new_password)
    db.commit()


def change_bio(db: Session, user: User, new_bio: str):
    user.bio = new_bio
    db.commit()


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()


# FetchLog

def save_fetched_data(db: Session, data: dict):
    obj = FetchLog(payload=data)
    db.add(obj)
    db.commit()


# Chat CRUD

def create_chat_session(db: Session, user_id: int) -> ChatSession:
    session = ChatSession(user_id=user_id)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_chat_sessions(db: Session, user_id: int):
    return db.query(ChatSession).filter(ChatSession.user_id == user_id).all()


def get_messages(db: Session, session_id: int):
    return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.timestamp).all()


def add_message(db: Session, session_id: int, sender: str, content: str) -> ChatMessage:
    msg = ChatMessage(session_id=session_id, sender=sender, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg
