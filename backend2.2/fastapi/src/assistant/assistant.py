import os
from dotenv import load_dotenv
import httpx

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

class ChatAssistant:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model

    def chat(self, user_message: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }
        response = httpx.post(OPENAI_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
