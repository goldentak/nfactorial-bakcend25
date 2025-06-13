import React, { useState, useEffect, useRef } from 'react';
import { getMessages, sendMessage, MessageRead } from '../../api/client';
import './chat.css';

interface ChatProps {
    sessionId: string;
}

const Chat: React.FC<ChatProps> = ({ sessionId }) => {
    const [messages, setMessages] = useState<MessageRead[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const endRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        getMessages(sessionId)
            .then(setMessages)
            .catch(console.error);
    }, [sessionId]);

    useEffect(() => {
        endRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSend = async () => {
        const text = input.trim();
        if (!text) return;
        setLoading(true);
        try {
            const userMsg = await sendMessage(sessionId, text);
            setMessages(ms => [...ms, userMsg]);
            const botMsg = await sendMessage(sessionId, text);
            setMessages(ms => [...ms, botMsg]);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
            setInput('');
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-messages">
                {messages.map(m => (
                    <div key={m.id} className={`message-bubble ${m.sender}`}>
                        {m.content}
                    </div>
                ))}
                {loading && (
                    <div className="message-bubble bot loading">typing...</div>
                )}
                <div ref={endRef} />
            </div>
            <div className="chat-input-area">
                <input
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyPress={e => e.key === 'Enter' && handleSend()}
                />
                <button onClick={handleSend} disabled={loading}>
                    Send
                </button>
            </div>
        </div>
    );
};

export default Chat;
