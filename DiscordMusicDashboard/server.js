// server.js

// Importing necessary libraries
const express = require('express');
const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');
const { Server } = require('socket.io');
const http = require('http');
const { playMusic, client } = require('./bot'); // Ensure the 'client' is exported from the 'bot.js' file

// Load environment variables
require('dotenv').config();

// Initialize Express app and HTTP server for Socket.IO
const app = express();
const server = http.createServer(app);
const io = new Server(server);

// Middleware to parse JSON bodies
app.use(express.json());

// MongoDB connection using environment variables
mongoose.connect(process.env.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => {
    console.log('MongoDB connected');
}).catch(err => {
    console.error('MongoDB connection error:', err);
});

// Authentication middleware to verify JWT tokens
function authenticateToken(req, res, next) {
    const authHeader = req.headers.authorization;
    const token = authHeader && authHeader.split(' ')[1]; // Extract token from Bearer
    if (!token) {
        return res.sendStatus(401); // Unauthorized if no token
    }

    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) {
            return res.sendStatus(403); // Forbidden if token is invalid
        }
        req.user = user;
        next();
    });
}

// Route for user login to provide JWT token
app.post('/api/login', (req, res) => {
    const { username } = req.body;
    if (!username) {
        return res.status(400).json({ error: 'Username is required' });
    }
    const user = { name: username };
    const accessToken = jwt.sign(user, process.env.JWT_SECRET, { expiresIn: '1h' });
    res.json({ accessToken });
});

// Setup Socket.IO for real-time interactions
io.on('connection', socket => {
    console.log('A user connected with Socket.IO');

    // Event listener for 'play' command to play music
    socket.on('play', async (url, voiceChannelId) => {
        const voiceChannel = client.channels.cache.get(voiceChannelId);
        if (voiceChannel) {
            try {
                const message = await playMusic(url, voiceChannel);
                socket.emit('status', message); // Emit status back to client
            } catch (error) {
                socket.emit('status', 'Failed to play music');
                console.error('Error playing music:', error);
            }
        } else {
            socket.emit('status', 'Voice channel not found'); // Error if voice channel does not exist
        }
    });
});

// Start the server on the specified port from environment variables or default to 5000
const PORT = process.env.PORT || 5000;
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
