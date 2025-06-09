import './login.css';
import { useState } from 'react';

interface LoginProps {
    onLogin: (username: string, password: string) => void;
    onRegister: (username: string, password: string) => void;
}

const Login: React.FC<LoginProps> = ({ onLogin, onRegister }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    return (
        <div className="login-container">
            <form className="login-form">
                <input
                    value={username}
                    type="text"
                    onChange={e => setUsername(e.target.value)}
                    placeholder="username"
                />
                <input
                    value={password}
                    type="password"
                    onChange={e => setPassword(e.target.value)}
                    placeholder="password"
                />
                <button type="button" onClick={() => onLogin(username, password)} className="login-form-btn">Login</button>
                <button type="button" onClick={() => onRegister(username, password)} className="register-form-btn">Register</button>
            </form>
        </div>
    );
};

export default Login;
