import { useEffect, useState } from 'react';
import AuthPage from './pages/AuthPage';
import HomePage from './pages/HomePage';
import { getAuthToken, getProfile, UserRead } from './api/client';

function App() {
    const [user, setUser] = useState<UserRead | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = getAuthToken();
        if (token) {
            getProfile()
                .then(setUser)
                .catch(() => {
                    localStorage.removeItem('jwt_token');
                    setUser(null);
                })
                .finally(() => setLoading(false));
        } else {
            setLoading(false);
        }
    }, []);

    if (loading) return <div>Loading...</div>;

    return user ? <HomePage user={user} setUser={setUser} /> : <AuthPage setUser={setUser} />;
}

export default App;
