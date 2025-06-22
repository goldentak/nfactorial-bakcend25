# Backend 2.4
AI voice assistant backend with web interface.

## Tech Stack
- Backend : FastAPI, Python
- Frontend : React, TypeScript
- Database : PostgreSQL
- Storage : AWS S3
- AI : Google Gemini
- TTS : ElevenLabs
## Project Structure
```
backend2.4/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── api/
├── frontend/
├── uploads/
└── requirements.txt
```

## API
### POST /api/voice/process
Request: ```json
{
"text": "Hello, how are you?",
"audio_file": "base64_encoded_audio"
}
```

Response: ```json
{
"ai_response": "Hello! I'm doing great, thanks!",
"ai_audio_url": " https://s3.amazonaws.com/bucket/audio.mp3 ",
"audio_available": true
}
```

## Setup
### Backend
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure environment (.env):
   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_BUCKET_NAME=your_bucket
   ELEVENLABS_API_KEY=your_elevenlabs_key
   GEMINI_API_KEY=your_gemini_key
   ```
3. Run server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
### Frontend
```bash
cd frontend
npm install
npm start
```

## Features
- 🎤 Voice recording
- 💬 Text processing
- 🤖 AI responses via Gemini
- 🔊 Speech synthesis via ElevenLabs
- ☁️ Audio storage in S3
## Test API
```bash
curl -X POST " http://localhost:8000/api/voice/process " -H "Content-Type: application/json" -d '{"text": "Hello!"}'
```

## Docker
```bash
docker-compose up -d
```
```
Server: http://localhost:8000 Frontend: http://localhost:3000 ```