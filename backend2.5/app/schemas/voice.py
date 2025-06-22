from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VoiceMessageResponse(BaseModel):
    id: int
    transcription: str
    ai_response: str
    file_path: str
    status: str
    created_at: Optional[datetime] = None

class VoiceProcessRequest(BaseModel):
    text: str
    voice_type: Optional[str] = "default"
    user_id: Optional[int] = None

class VoiceMessageCreate(BaseModel):
    transcription: str
    ai_response: str
    file_path: str
    user_id: Optional[int] = None