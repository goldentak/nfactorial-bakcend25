from fastapi import FastAPI
import uvicorn

from src.database import engine, Base
from src.routers.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Hello, FastAPI with Postgres!"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
