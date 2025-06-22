from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import os
import uuid
import logging
from app.database import get_db, engine
from app.models import models
from app.models.models import User, VoiceMessage
from app.config import settings
from app.services.ai_service import AIService
from app.services.s3_service import S3Service
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Voice Message API",
    description="Comprehensive backend system with CRUD, WebSocket, S3, and more",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/voice/generated", exist_ok=True)
os.makedirs("uploads/chat_audio", exist_ok=True)

# Mount static files BEFORE defining routes
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/voice/upload")
async def upload_voice_message(
    file: UploadFile = File(...),
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    try:
        if not file.content_type or not file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Handle user_id - create default user if none exists
        if user_id is None:
            # Check if any user exists, if not create one
            existing_user = db.query(models.User).first()
            if not existing_user:
                default_user = models.User(
                    username='default_user',
                    email='default@example.com',
                    hashed_password='dummy_hash',
                    is_active=True
                )
                db.add(default_user)
                db.commit()
                db.refresh(default_user)
                user_id = default_user.id
            else:
                user_id = existing_user.id
        
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'mp3'
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = f"uploads/{unique_filename}"
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        from app.services.ai_service import AIService
        ai_service = AIService()
        
        transcription = await ai_service.transcribe_audio(file_path)
        ai_response = await ai_service.process_voice_message(transcription, user_id)
        
        ai_audio_path = None
        try:
            ai_audio_path = await ai_service.text_to_speech_openai(ai_response)
        except Exception as openai_error:
            try:
                ai_audio_path = await ai_service.text_to_speech_elevenlabs(ai_response)
            except Exception as elevenlabs_error:
                print(f"TTS failed - OpenAI: {openai_error}, ElevenLabs: {elevenlabs_error}")
        
        voice_message = models.VoiceMessage(
            user_id=user_id,  # Remove the "or 1" fallback
            file_path=file_path,
            original_filename=file.filename,
            transcription=transcription,
            ai_response=ai_response,
            ai_audio_path=ai_audio_path
        )
        
        db.add(voice_message)
        db.commit()
        db.refresh(voice_message)
        
        return {
            "message": "Voice message processed successfully",
            "message_id": voice_message.id,
            "transcription": transcription,
            "ai_response": ai_response,
            "ai_audio_url": f"/api/v1/voice/audio/{os.path.basename(ai_audio_path)}" if ai_audio_path else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing voice message: {str(e)}")

@app.get("/api/v1/voice/audio/{filename}")
async def get_audio_file(filename: str):
    file_path = f"uploads/chat_audio/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    raise HTTPException(status_code=404, detail="Audio file not found")

@app.get("/api/v1/voice/history")
async def get_message_history(
    user_id: Optional[int] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(models.VoiceMessage)
    if user_id:
        query = query.filter(models.VoiceMessage.user_id == user_id)
    
    messages = query.order_by(models.VoiceMessage.created_at.desc()).limit(limit).all()
    
    return {
        "messages": [
            {
                "id": msg.id,
                "transcription": msg.transcription,
                "ai_response": msg.ai_response,
                "ai_audio_url": f"/api/v1/voice/audio/{os.path.basename(msg.ai_audio_path)}" if msg.ai_audio_path else None,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    }

class TextToSpeechRequest(BaseModel):
    text: str
    user_id: Optional[int] = None

@app.post("/api/v1/text/chat")
async def text_to_speech_chat(request: TextToSpeechRequest, db: Session = Depends(get_db)):
    try:
        user_id = request.user_id or 0
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            user = User(
                id=user_id, 
                username=f"user_{user_id}",
                email=f"user_{user_id}@example.com",
                hashed_password="default_hash"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        ai_service = AIService()
        
        ai_response = await ai_service.process_text_message(request.text, user_id)
        
        ai_audio_url = None
        audio_available = False
        
        try:
            if settings.elevenlabs_api_key:
                audio_content = await ai_service.text_to_speech_elevenlabs(ai_response)
                
                # --- TEMPORARY LOCAL STORAGE --- 
                if audio_content:
                    filename = f"{uuid.uuid4()}.mp3"
                    os.makedirs("uploads/chat_audio", exist_ok=True)
                    file_path = f"uploads/chat_audio/{filename}"
                    with open(file_path, "wb") as f:
                        f.write(audio_content)
                    
                    ai_audio_url = f"/api/v1/voice/audio/{filename}"
                    audio_available = True
                    logger.info(f"Audio saved locally: {ai_audio_url}")
                # --- END TEMPORARY LOCAL STORAGE ---
                # if settings.aws_access_key_id and audio_content:
                #     s3_service = S3Service()
                #     filename = f"chat_audio/{uuid.uuid4()}.mp3"
                #     ai_audio_url = await s3_service.upload_audio_file(audio_content, filename)
                #     audio_available = True
                #     logger.info(f"Audio uploaded to S3: {ai_audio_url}")
                else:
                    logger.warning("Audio generation failed")
            else:
                logger.warning("ElevenLabs API key not configured")
        except Exception as e:
            logger.error(f"TTS or S3 upload failed: {str(e)}")
        
        voice_message = VoiceMessage(
            user_id=user.id,
            original_filename="text_input",
            transcription=request.text,
            ai_response=ai_response,
            ai_audio_path=ai_audio_url
        )
        
        db.add(voice_message)
        db.commit()
        db.refresh(voice_message)
        
        return {
            "message": "Text processed successfully",
            "message_id": voice_message.id,
            "user_text": request.text,
            "ai_response": ai_response,
            "ai_audio_url": ai_audio_url,
            "audio_available": audio_available
        }
        
    except Exception as e:
        logger.error(f"Text chat error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
