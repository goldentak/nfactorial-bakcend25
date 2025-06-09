from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed)
    db.add(db_user); db.commit(); db.refresh(db_user)
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