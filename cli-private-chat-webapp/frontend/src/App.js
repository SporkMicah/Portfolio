import React, { useState } from 'react';
import axios from 'axios';
import Chat from './components/Chat';
import './App.css';

function App() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [token, setToken] = useState('');
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const handleRegister = async() => {
        try {
            await axios.post(`${process.env.REACT_APP_SERVER_URL}/api/auth/register`, { username, password});
            alert('User registered successfully');
        } catch (error) {
            console.error('Registration error:', error);
            alert('Error registering user');
        }
    };

    const handleLogin = async () => {
        try {
            const response = await axios.post(`${process.env.REACT_APP_SERVER_URL}/api/auth/login`, { username, password});
            setToken(response.data.token);
            setIsAuthenticated(true);
        } catch (error) {
            console.error('Login error:', error);
            alert('Error logging in');
        }
    };

    return (
        <div className="App">
          {!isAuthenticated ? (
            <div>
              <h1>Login/Register</h1>
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <button onClick={handleRegister}>Register</button>
              <button onClick={handleLogin}>Login</button>
            </div>
          ) : (
            <Chat />
          )}
        </div>
      );
    }
    
    export default App;