import React, { useState } from 'react';
import Home from '../components/Home';

const HomePage: React.FC = () => {
    const [user, setUser] = useState({ username: 'Alice', bio: 'I love coding!' });

    const handleChangeUsername = (newUsername: string) => {
        setUser(u => ({ ...u, username: newUsername }));
    };
    const handleChangePassword = () => alert('Change password');
    const handleDeleteUsername = () => alert('Delete account');
    const handleLogout = () => alert('Logout');
    const handleChangeBio = (newBio: string) => setUser(u => ({ ...u, bio: newBio }));

    return (
        <div>
            <Home
                user={user}
                onChangeUsername={handleChangeUsername}
                onChangePassword={handleChangePassword}
                onDeleteUsername={handleDeleteUsername}
                onLogout={handleLogout}
                onChangeBio={handleChangeBio}
            />
        </div>
    );
};

export default HomePage;
