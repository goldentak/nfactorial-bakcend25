import sqlite3
import uuid
from datetime import datetime
from typing import List, Dict, Optional

class SQLiteStorage:
    def __init__(self, db_path: str = "voice_messages.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS voice_messages (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                original_filename TEXT,
                file_path TEXT,
                transcription TEXT,
                ai_response TEXT,
                ai_audio_path TEXT,
                created_at TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def save_voice_message(self, user_id: str, original_filename: str, 
                          file_path: str, transcription: str = None, 
                          ai_response: str = None, ai_audio_path: str = None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        message_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO voice_messages 
            (id, user_id, original_filename, file_path, transcription, ai_response, ai_audio_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (message_id, user_id, original_filename, file_path, transcription, 
              ai_response, ai_audio_path, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        return message_id