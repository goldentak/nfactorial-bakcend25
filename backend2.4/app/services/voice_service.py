import asyncio
from sqlalchemy.orm import Session
from app.models.models import VoiceMessage
from app.schemas.voice import VoiceMessageCreate
from typing import List, Optional

class VoiceService:
    def __init__(self):
        pass
        
    async def save_voice_message(
        self, 
        db: Session, 
        file_path: str, 
        transcription: str, 
        ai_response: str, 
        ai_audio_path: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> VoiceMessage:
        voice_message = VoiceMessage(
            file_path=file_path,
            transcription=transcription,
            ai_response=ai_response,
            ai_audio_path=ai_audio_path,
            user_id=user_id
        )
        db.add(voice_message)
        db.commit()
        db.refresh(voice_message)
        return voice_message
    
    async def get_user_voice_history(self, db: Session, user_id: int) -> List[dict]:
        messages = db.query(VoiceMessage).filter(
            VoiceMessage.user_id == user_id
        ).order_by(VoiceMessage.created_at.desc()).limit(50).all()
        
        return [
            {
                "id": msg.id,
                "transcription": msg.transcription,
                "ai_response": msg.ai_response,
                "ai_audio_path": msg.ai_audio_path,
                "created_at": msg.created_at
            }
            for msg in messages
        ]