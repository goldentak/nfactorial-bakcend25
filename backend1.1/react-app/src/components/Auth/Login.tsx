import './login.css'


const Login = () => {
    return (
        <div className="login-container">
            <form action="" className="login-form">
                <input type="text" placeholder="username"  />
                <input type="password" placeholder="password" />
                <input type="submit" value="Login" />
            </form>
        </div>
    );
};

export default Login;