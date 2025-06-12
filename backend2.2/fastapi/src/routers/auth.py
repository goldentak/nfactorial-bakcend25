from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.models import User

from .. import crud, schemas, database, config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter(prefix="/auth", tags=["auth"])

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    now = datetime.utcnow()
    to_encode.update({"iat": now})
    if expires_delta:
        to_encode.update({"exp": now + expires_delta})
    token = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return token

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db)
):
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exc
    except JWTError:
        raise credentials_exc

    user = crud.get_user_by_username(db, username)
    if not user:
        raise credentials_exc
    return user

@router.post("/register", response_model=schemas.UserRead)
def register(
    user: schemas.UserCreate = Body(...),
    db: Session = Depends(database.get_db)
):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)

@router.post("/login", response_model=schemas.Token)
def login(
    credentials: schemas.UserCreate = Body(...),
    db: Session = Depends(database.get_db)
):
    user = crud.authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    access_token = create_access_token(
        {"sub": user.username},
        expires_delta=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/user", response_model=schemas.UserRead)
def read_user(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.patch("/user", response_model=schemas.UserRead)
def update_user(
    username: str = Body(default=None),
    password: str = Body(default=None),
    bio: str = Body(default=None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    if username:
        crud.change_username(db, current_user, username)
    if password:
        crud.change_password(db, current_user, password)
    if bio is not None:
        crud.change_bio(db, current_user, bio)
    db.refresh(current_user)
    return current_user

@router.delete("/user")
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    crud.delete_user(db, current_user)
    return {"msg": "User account deleted"}

@router.post("/logout")
def logout():
    return {"msg": "Logged out"}
