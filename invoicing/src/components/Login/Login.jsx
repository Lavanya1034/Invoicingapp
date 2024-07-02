import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        console.log(username)
        console.log(password)
        try {
            const response = await fetch('http://localhost:8000/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                

                body: JSON.stringify({ username, password }),
            });
            const data = await response.json();
            console.log(data)
            if (!data.access_token) {
                alert("Login Failed");
            }
            else {
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('refresh', data.refresh_token);
                navigate("/");
            }
        } catch (error) {
            console.error('Error logging in:', error);
        }
    };

    return (
        <div className="container d-flex justify-content-center align-items-center vh-100" style={{ maxWidth: "700px" }}>
            <form className="p-4 border shadow w-100">
                <div className="mb-3">
                    <label htmlFor="username" className="form-label">Username:</label>
                    <input
                        type="text"
                        id="username"
                        className="form-control"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">Password:</label>
                    <input
                        type="password"
                        id="password"
                        className="form-control"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button type="button" className="btn btn-primary" onClick={handleLogin}>
                    Login
                </button>
            </form>
        </div>
    );
};

export default Login;