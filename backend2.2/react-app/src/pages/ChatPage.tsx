import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import Chat from '../components/Chat/Chat';
import './chatPage.css';
import { getSessions, createSession } from '../api/client';

export default function ChatPage() {
    const navigate = useNavigate();
    const { sessionId } = useParams<{ sessionId: string }>();
    const [sessions, setSessions] = useState<{ id: number; created_at: string }[]>([]);

    useEffect(() => {
        getSessions().then(setSessions).catch(console.error);
    }, []);

    function handleNew() {
        createSession()
            .then(s => {
                setSessions(prev => [...prev, s]);
                navigate(`/chat/${s.id}`);
            })
            .catch(console.error);
    }

    return (
        <div className="chat-page">
            <aside className="chat-list">
                <button className="smallButton" onClick={() => navigate('/')}>Home</button>
                <button className="smallButton" onClick={handleNew}>+ New Chat</button>
                {sessions.map(s => (
                    <Link key={s.id} to={`/chat/${s.id}`} className="chat-link">
                        Session #{s.id}
                    </Link>
                ))}
            </aside>
            <main className="chat-window">
                {sessionId
                    ? <Chat sessionId={sessionId} />
                    : <div className="select">Select a chat</div>}
            </main>
        </div>
    );
}