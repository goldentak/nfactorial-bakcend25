import React from 'react';
import { useNavigate } from 'react-router-dom';
import Home from '../components/Home';
import {
    updateProfile,
    logout,
    deleteUser,
    UserRead,
} from '../api/client';
import styles from '../components/Home.module.css';

interface Props {
    user: UserRead;
    setUser: React.Dispatch<React.SetStateAction<UserRead | null>>;
}

const HomePage: React.FC<Props> = ({ user, setUser }) => {
    const nav = useNavigate();

    const changeUsername = async (name: string) => {
        const updated = await updateProfile({ username: name });
        setUser(updated);
    };

    const changePassword = async () => {
        const pwd = prompt('New password');
        if (!pwd) return;
        await updateProfile({ password: pwd });
        alert('Password updated');
    };

    const changeBio = async (bio: string) => {
        const updated = await updateProfile({ bio });
        setUser(updated);
    };

    const doLogout = () => {
        logout();
        setUser(null);
    };

    const doDelete = async () => {
        if (!window.confirm('Delete account?')) return;
        await deleteUser();
        setUser(null);
    };

    return (
        <div className={styles.container}>
            <button
                className={styles.chatNavButton}
                onClick={() => nav('/chat')}
            >
                Go to Chat
            </button>
            <Home
                user={user}
                onChangeUsername={changeUsername}
                onChangePassword={changePassword}
                onChangeBio={changeBio}
                onLogout={doLogout}
                onDeleteAccount={doDelete}
            />
        </div>
    );
};

export default HomePage;
