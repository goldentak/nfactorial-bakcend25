import React from 'react';
import { Routes, Route, Navigate, Link } from 'react-router-dom';
import AuthPage from './pages/AuthPage';
import HomePage from './pages/HomePage';
import ChatPage from './pages/ChatPage';
import { getAuthToken, getProfile, UserRead } from './api/client';

const App: React.FC = () => {
    const [user, setUser] = React.useState<UserRead | null>(null);
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {
        const token = getAuthToken();
        if (token) {
            getProfile()
                .then(setUser)
                .catch(() => setUser(null))
                .finally(() => setLoading(false));
        } else setLoading(false);
    }, []);

    if (loading) return <div>Loading...</div>;

    if (!user) return <AuthPage setUser={setUser} />;
    return (
        <Routes>
            <Route path="/" element={<HomePage user={user} setUser={setUser} />} />
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/chat/:sessionId" element={<ChatPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
    );
};

export default App;