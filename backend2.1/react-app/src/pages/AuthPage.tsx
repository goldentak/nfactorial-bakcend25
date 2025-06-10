import React from 'react';
import Login from '../components/Auth/Login';
import { login, register, getProfile, UserRead } from '../api/client';

interface AuthPageProps {
    setUser: (user: UserRead) => void;
}

const AuthPage: React.FC<AuthPageProps> = ({ setUser }) => {
    const handleLogin = async (username: string, password: string) => {
        try {
            await login(username, password);
            const user = await getProfile();
            setUser(user);
        } catch (e: any) {
            alert(`Login failed: ${e.message}`);
        }
    };

    const handleRegister = async (username: string, password: string) => {
        try {
            await register(username, password);
            await handleLogin(username, password);
        } catch (e: any) {
            alert(`Registration failed: ${e.message}`);
        }
    };

    return <Login onLogin={handleLogin} onRegister={handleRegister} />;
};

export default AuthPage;
