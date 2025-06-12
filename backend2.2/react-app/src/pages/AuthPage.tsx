import React from 'react';
import { useNavigate } from 'react-router-dom';
import Login from '../components/Auth/Login';
import { login, register, getProfile, UserRead } from '../api/client';

interface Props { setUser: React.Dispatch<React.SetStateAction<UserRead | null>>; }

const AuthPage: React.FC<Props> = ({ setUser }) => {
    const nav = useNavigate();

    const handleLogin = async (u: string, p: string) => {
        try {
            await login(u, p);
            const me = await getProfile();
            setUser(me);
            nav('/');
        } catch (e: any) {
            alert(`Login failed: ${e.message}`);
        }
    };

    const handleRegister = async (u: string, p: string) => {
        try {
            await register(u, p);
            alert('Registered! Now please login.');
        } catch (e: any) {
            alert(`Registration failed: ${e.message}`);
        }
    };

    return <Login onLogin={handleLogin} onRegister={handleRegister} />;
};

export default AuthPage;
