from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import aiofiles
import uuid
import os
from typing import Optional

from app.database import get_db
from app.services.voice_service import VoiceService
from app.services.ai_service import AIService
from app.schemas.voice import VoiceMessageResponse, VoiceProcessRequest

router = APIRouter()
voice_service = VoiceService()
ai_service = AIService()

@router.post("/upload", response_model=VoiceMessageResponse)
async def upload_voice_message(
    audio_file: UploadFile = File(...),
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Загрузка голосового сообщения и отправка его на обработку ИИ
    """
    try:
        # Проверка типа файла
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="Файл должен быть аудио")
        
        # Сохранение файла
        file_id = str(uuid.uuid4())
        file_path = f"uploads/voice/{file_id}_{audio_file.filename}"
        
        os.makedirs("uploads/voice", exist_ok=True)
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await audio_file.read()
            await f.write(content)
        
        # Обработка голосового сообщения
        transcription = await voice_service.transcribe_audio(file_path)
        
        # Отправка в ИИ для обработки
        ai_response = await ai_service.process_voice_message(
            transcription=transcription,
            user_id=user_id
        )
        
        # Сохранение в базу данных
        voice_record = await voice_service.save_voice_message(
            db=db,
            file_path=file_path,
            transcription=transcription,
            ai_response=ai_response,
            user_id=user_id
        )
        
        return VoiceMessageResponse(
            id=voice_record.id,
            transcription=transcription,
            ai_response=ai_response,
            file_path=file_path,
            status="processed"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки: {str(e)}")

@router.post("/process-text")
async def process_text_to_speech(
    request: VoiceProcessRequest,
    db: Session = Depends(get_db)
):
    """
    Преобразование текста в голосовое сообщение
    """
    try:
        # Генерация голосового ответа
        audio_file_path = await voice_service.text_to_speech(
            text=request.text,
            voice_type=request.voice_type
        )
        
        return {
            "audio_url": f"/api/v1/voice/audio/{os.path.basename(audio_file_path)}",
            "text": request.text,
            "status": "generated"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации: {str(e)}")

@router.get("/audio/{filename}")
async def get_audio_file(filename: str):
    """
    Получение аудио файла
    """
    file_path = f"uploads/voice/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    return FileResponse(file_path)

@router.get("/history/{user_id}")
async def get_voice_history(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Получение истории голосовых сообщений пользователя
    """
    history = await voice_service.get_user_voice_history(db, user_id)
    return {"history": history}