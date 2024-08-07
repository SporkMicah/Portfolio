// App.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import io from 'socket.io-client';
import './App.css';

// Establish a connection to the server using Socket.IO
const socket = io(process.env.REACT_APP_SERVER_URL);

function App() {
  const [username, setUsername] = useState('');
  const [token, setToken] = useState('');
  const [city, setCity] = useState('');
  const [weather, setWeather] = useState('');
  const [status, setStatus] = useState('');

  // Register socket event listeners only once on component mount
  useEffect(() => {
    const handleStatus = (message) => setStatus(message);
    socket.on('status', handleStatus);

    // Cleanup function to unsubscribe from events on component unmount
    return () => {
      socket.off('status', handleStatus);
    };
  }, []);

  // Handles user login, requests a JWT token from the server
  const handleLogin = async () => {
    try {
      const response = await axios.post(`${process.env.REACT_APP_SERVER_URL}/api/login`, { username });
      setToken(response.data.accessToken);
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  // Fetches weather information for the specified city
  const handleGetWeather = async () => {
    if (city && token) {
      try {
        const response = await axios.get(`${process.env.REACT_APP_SERVER_URL}/api/weather`, {
          headers: { Authorization: `Bearer ${token}` },
          params: { city }
        });
        setWeather(response.data);
      } catch (error) {
        console.error('Weather fetch error:', error);
      }
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Discord YT Music Dashboard</h1>
        <div>
          <input
            type="text"
            placeholder="Enter your username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <button onClick={handleLogin}>Login</button>
        </div>
        <div>
          <input
            type="text"
            placeholder="Enter city name"
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />
          <button onClick={handleGetWeather}>Get Weather</button>
        </div>
        <div>
          {weather && <p>{weather}</p>}
          {status && <p>{status}</p>}
        </div>
      </header>
    </div>
  );
}

export default App;
