import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class LocalJSONStorage:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def save_voice_message(self, user_id: str, original_filename: str, 
                          file_path: str, transcription: str = None, 
                          ai_response: str = None, ai_audio_path: str = None):
        voice_data = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "original_filename": original_filename,
            "file_path": file_path,
            "transcription": transcription,
            "ai_response": ai_response,
            "ai_audio_path": ai_audio_path,
            "created_at": datetime.now().isoformat()
        }
        
        file_path = os.path.join(self.data_dir, f"voice_messages_{user_id}.json")
        messages = self.load_user_messages(user_id)
        messages.append(voice_data)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        
        return voice_data
    
    def load_user_messages(self, user_id: str) -> List[Dict]:
        file_path = os.path.join(self.data_dir, f"voice_messages_{user_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []