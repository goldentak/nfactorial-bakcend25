import React, { useState, useRef } from 'react';
import './App.css';

interface ApiResponse {
  message: string;
  ai_response: string;
  ai_audio_url: string | null;
  audio_available: boolean;
}

function App() {
  const [text, setText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const audioRef = useRef<HTMLAudioElement>(null);

  const API_BASE_URL = 'http://localhost:8000';

  const playAudio = async (audioUrl: string) => {
    if (audioRef.current) {
      try {
        let fullUrl;
        if (audioUrl.startsWith('http')) {
          fullUrl = audioUrl;
        } else {
          const filename = audioUrl.split('/').pop() || audioUrl;
          fullUrl = `${API_BASE_URL}/uploads/chat_audio/${filename}`;
        }
        
        console.log('Playing audio from:', fullUrl);
        audioRef.current.src = fullUrl;
        await audioRef.current.load();
        await audioRef.current.play();
      } catch (err) {
        console.error('Audio playback failed:', err);
        setError('Failed to play audio');
      }
    }
  };

  const handleTextSubmit = async () => {
    if (!text.trim()) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/text/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, user_id: 1 }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to send text');
      }
      
      const data: ApiResponse = await response.json();
      setResponse(data);
      
      if (data.ai_audio_url) {
        await playAudio(data.ai_audio_url);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];
      
      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };
      
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        await uploadAudio(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      setError('Failed to access microphone');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const uploadAudio = async (audioBlob: Blob) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append('file', audioBlob, 'recording.wav');
      formData.append('user_id', '1');
      
      const response = await fetch(`${API_BASE_URL}/api/v1/voice/upload`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Failed to upload audio');
      }
      
      const data = await response.json();
      setResponse({
        message: data.message,
        ai_response: data.ai_response,
        ai_audio_url: data.ai_audio_url,
        audio_available: !!data.ai_audio_url
      });
      
      if (data.ai_audio_url) {
        await playAudio(data.ai_audio_url);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Voice Assistant</h1>
        
        <div className="input-section">
          <div className="text-input">
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter your text here..."
              rows={4}
              cols={50}
            />
            <button 
              onClick={handleTextSubmit} 
              disabled={isLoading || !text.trim()}
            >
              {isLoading ? 'Processing...' : 'Send Text'}
            </button>
          </div>
          
          <div className="voice-input">
            <button
              onClick={isRecording ? stopRecording : startRecording}
              disabled={isLoading}
              className={isRecording ? 'recording' : ''}
            >
              {isRecording ? 'Stop Recording' : 'Start Recording'}
            </button>
          </div>
        </div>
        
        {error && (
          <div className="error">
            Error: {error}
          </div>
        )}
        
        {response && (
          <div className="response">
            <h3>AI Response:</h3>
            <p>{response.ai_response}</p>
            {response.audio_available && (
              <div className="audio-player">
                <audio ref={audioRef} controls preload="metadata">
                  Your browser does not support the audio element.
                </audio>
                <button 
                  onClick={() => response.ai_audio_url && playAudio(response.ai_audio_url)}
                  disabled={!response.ai_audio_url}
                >
                  Play Audio
                </button>
              </div>
            )}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
