import asyncio
import requests
import uuid
import os
import logging
from typing import Optional
from app.config import settings

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        logger.info("Initializing AIService")
        self.gemini_model = None
        
        if (GEMINI_AVAILABLE and 
            hasattr(settings, 'gemini_api_key') and 
            settings.gemini_api_key and 
            settings.gemini_api_key.strip()):
            try:
                genai.configure(api_key=settings.gemini_api_key.strip())
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("Gemini client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                self.gemini_model = None
        else:
            logger.warning("Gemini not available or API key not configured")
    
    async def transcribe_audio(self, audio_file_path: str) -> str:
        try:
            logger.info(f"Starting transcription for file: {audio_file_path}")
            
            if not self.gemini_model:
                logger.warning("Gemini client not initialized")
                return "Audio transcription not available - Gemini API key not configured"
            
            logger.warning("Gemini doesn't support audio transcription directly")
            return "Audio transcription not available - Gemini doesn't support audio transcription"
            
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            return f"Transcription error: {str(e)}"
    
    async def process_voice_message(
        self, 
        transcription: str, 
        user_id: Optional[int] = None
    ) -> str:
        try:
            logger.info(f"Processing voice message for user {user_id}: {transcription[:50]}...")
            
            if not self.gemini_model:
                logger.warning("Gemini client not initialized, using simple response")
                return self._generate_simple_response(transcription)
            
            prompt = f"You are a helpful voice assistant. Respond naturally and conversationally to this voice message: {transcription}"
            
            response = self.gemini_model.generate_content(prompt)
            
            ai_response = response.text
            logger.info(f"AI response generated: {ai_response[:50]}...")
            return ai_response
            
        except Exception as e:
            logger.error(f"AI processing error: {str(e)}")
            return self._generate_simple_response(transcription)
    
    async def process_text_message(self, text: str, user_id: Optional[int] = None) -> str:
        try:
            logger.info(f"Processing text message for user {user_id}: {text[:50]}...")
            
            if not self.gemini_model:
                logger.warning("Gemini client not initialized")
                return "AI service not available - Gemini API key not configured"
            
            prompt = f"You are a friendly and natural conversational AI assistant. Respond to this message in a casual, helpful way: {text}"
            
            response = self.gemini_model.generate_content(prompt)
            ai_response = response.text
            
            logger.info(f"AI response generated: {ai_response[:50]}...")
            return ai_response
            
        except Exception as e:
            logger.error(f"AI processing error: {str(e)}")
            return "Sorry, I encountered an error processing your message."
    
    async def text_to_speech_elevenlabs(self, text: str) -> bytes:
        try:
            if not settings.elevenlabs_api_key:
                raise Exception("ElevenLabs API key not configured")
            
            logger.info(f"Starting ElevenLabs TTS for text: {text[:50]}...")
            
            voice_id = "21m00Tcm4TlvDq8ikWAM"
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": settings.elevenlabs_api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                logger.info("ElevenLabs TTS successful")
                return response.content
            else:
                error_msg = f"ElevenLabs API error: {response.status_code}"
                if response.text:
                    error_msg += f" - {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {str(e)}")
            raise Exception(f"ElevenLabs TTS error: {str(e)}")
    
    def _generate_simple_response(self, transcription: str) -> str:
        if "transcription not available" in transcription.lower():
            return "I received your voice message, but I cannot transcribe it without proper API configuration. Please configure your API keys."
        return f"I heard you say: '{transcription}'. This is a simple response since AI services are not configured."