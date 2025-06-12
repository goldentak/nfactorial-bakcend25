import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "postgresql://postgres:3245@db:5432/postgres"

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "CHANGE_ME_IN_PROD")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
