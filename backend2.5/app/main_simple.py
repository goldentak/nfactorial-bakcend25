from fastapi import FastAPI, UploadFile, File, HTTPException
from app.services.local_storage import LocalJSONStorage
from app.services.ai_service import AIService
import uuid
import os
import aiofiles

app = FastAPI()
storage = LocalJSONStorage()
ai_service = AIService()

@app.post("/api/v1/voice/upload")
async def upload_voice_message(file: UploadFile = File(...), user_id: str = "default_user"):
    if not file.filename.endswith(('.mp3', '.wav', '.m4a')):
        raise HTTPException(status_code=400, detail="Unsupported file format")
    
    file_id = str(uuid.uuid4())
    file_extension = file.filename.split('.')[-1]
    file_path = f"uploads/{file_id}.{file_extension}"
    
    os.makedirs("uploads", exist_ok=True)
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    transcription = await ai_service.transcribe_audio(file_path)
    ai_response = await ai_service.process_text(transcription)
    ai_audio_path = await ai_service.text_to_speech(ai_response)
    
    voice_message = storage.save_voice_message(
        user_id=user_id,
        original_filename=file.filename,
        file_path=file_path,
        transcription=transcription,
        ai_response=ai_response,
        ai_audio_path=ai_audio_path
    )
    
    return {
        "message": "Voice message processed successfully",
        "transcription": transcription,
        "ai_response": ai_response,
        "ai_audio_url": f"/audio/{os.path.basename(ai_audio_path)}"
    }

@app.get("/history/{user_id}")
async def get_user_history(user_id: str):
    messages = storage.load_user_messages(user_id)
    return {"messages": messages}