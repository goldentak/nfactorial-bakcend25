import React from 'react';
import Home from '../components/Home';
import { updateProfile, logout, deleteUser, UserRead } from '../api/client';

interface HomePageProps {
    user: UserRead;
    setUser: React.Dispatch<React.SetStateAction<UserRead | null>>;
}

const HomePage: React.FC<HomePageProps> = ({ user, setUser }) => {

    const handleChangeUsername = async (newUsername: string) => {
        try {
            const updatedUser = await updateProfile({ username: newUsername });
            setUser(updatedUser);
        } catch (e: any) {
            alert(`Failed to update username: ${e.message}`);
        }
    };

    const handleChangePassword = async () => {
        const newPassword = prompt('Enter new password');
        if (newPassword) {
            try {
                await updateProfile({ password: newPassword });
                alert('Password updated successfully.');
            } catch (e: any) {
                alert(`Failed to update password: ${e.message}`);
            }
        }
    };

    const handleChangeBio = async (newBio: string) => {
        try {
            const updatedUser = await updateProfile({ bio: newBio });
            setUser(updatedUser);
        } catch (e: any) {
            alert(`Failed to update bio: ${e.message}`);
        }
    };

    const handleLogout = () => {
        logout().finally(() => {
            setUser(null);
        });
    };

    const handleDeleteAccount = async () => {
        if (confirm("Are you sure you want to delete your account? This action cannot be undone.")) {
            try {
                await deleteUser();
                alert('Your account has been successfully deleted.');
                setUser(null);
            } catch (err: any) {
                alert(`Failed to delete account: ${err.message}`);
            }
        }
    };

    return (
        <Home
            user={user}
            onChangeUsername={handleChangeUsername}
            onChangePassword={handleChangePassword}
            onChangeBio={handleChangeBio}
            onLogout={handleLogout}
            onDeleteAccount={handleDeleteAccount}
        />
    );
};

export default HomePage;
