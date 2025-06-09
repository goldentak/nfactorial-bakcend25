import React, { useState } from 'react';
import styles from './Home.module.css';

type User = {
    username: string;
    bio: string;
};

interface HomeProps {
    user: User;
    onChangeUsername: (newUsername: string) => void;
    onChangePassword: () => void;
    onChangeBio: (newBio: string) => void;
}

const Home: React.FC<HomeProps> = ({ user, onChangeUsername, onChangePassword, onChangeBio }) => {
    if (!user) throw new Error('User prop is required');

    const [editingUsername, setEditingUsername] = useState(false);
    const [newUsername, setNewUsername] = useState(user.username);
    const [editingBio, setEditingBio] = useState(false);
    const [newBio, setNewBio] = useState(user.bio);

    return (
        <div className={styles.container}>
            <div className={styles.topSection}>
                <div className={styles.avatarPlaceholder} />
                {editingUsername ? (
                    <input
                        className={styles.usernameText}
                        value={newUsername}
                        onChange={e => setNewUsername(e.target.value)}
                        style={{
                            padding: '0.8rem',
                            borderRadius: '4px',
                            border: '1px solid #444',
                            background: '#121212',
                            color: '#fff',
                            fontSize: '1.75rem'
                        }}
                    />
                ) : (
                    <div className={styles.usernameText}>{user.username}</div>
                )}
                <div className={styles.buttonGroup}>
                    {editingUsername ? (
                        <button
                            className={styles.smallButton}
                            onClick={() => { onChangeUsername(newUsername); setEditingUsername(false); }}
                        >
                            Save
                        </button>
                    ) : (
                        <button
                            className={styles.smallButton}
                            onClick={() => setEditingUsername(true)}
                        >
                            Change Username
                        </button>
                    )}
                    <button
                        className={styles.smallButton}
                        onClick={onChangePassword}
                    >
                        Change Password
                    </button>
                </div>
            </div>

            <div className={styles.bottomSection}>
                <div className={styles.bioBox}>
                    {editingBio ? (
                        <textarea
                            style={{
                                width: '100%',
                                height: '100%',
                                background: '#1e1e1e',
                                color: '#fff',
                                border: '1px solid #444',
                                borderRadius: '4px',
                                padding: '0.75rem',
                                fontSize: '1rem'
                            }}
                            value={newBio}
                            onChange={e => setNewBio(e.target.value)}
                        />
                    ) : (
                        user.bio || 'No bio available.'
                    )}
                </div>
                {editingBio ? (
                    <button
                        className={styles.changeBioButton}
                        onClick={() => { onChangeBio(newBio); setEditingBio(false); }}
                    >
                        Save Bio
                    </button>
                ) : (
                    <button
                        className={styles.changeBioButton}
                        onClick={() => setEditingBio(true)}
                    >
                        Change Bio
                    </button>
                )}
            </div>
        </div>
    );
};

export default Home;
