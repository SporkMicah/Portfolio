const express = require('express');
const net = require('net');
const app = express();
const PORT = 3000;

app.use(express.json()); // Middleware to parse JSON bodies

app.post('/scan', (req, res) => {
    const { hostname, port } = req.body;
    const socket = new net.Socket();
    const timeout = 2000; // 2 seconds timeout

    socket.setTimeout(timeout);
    socket.on('timeout', () => {
        socket.end();
        res.send(`Port ${port} is closed (timeout).`);
    });

    socket.connect(port, hostname, () => {
        res.send(`Port ${port} is open.`);
        socket.end();
    });

    socket.on('error', (err) => {
        res.send(`Port ${port} is closed (${err.message}).`);
    });
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});