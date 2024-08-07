import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

// Initialize socket connection using the server URL from environment variables
const socket = io(process.env.REACT_APP_SERVER_URL);

function Chat() {
    // State hook for current message input 
    const [message, setMessage] = useState('');
    //State hook for storing all messages received
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        // Function to handle new incoming messages
        const handleNewMessage = (msg) =>{
            // Update the messages array by appending the new message
            setMessages((prevMessages) => [...prevMessages, msg]);
        };

        // Register the event listener for receiving new messages
        socket.on('message', handleNewMessage);

        // Cleanup function to remove the event listener when the component unmounts or the dependency array changes
        return () => {
            socket.off('message', handleNewMessage);
        };
    }, []); // Empty dependency array means this effect only runs once after the initial render

    const sendMessage = () => {
        // Prevent sending an empty message
        if (!message) return;
        // Emit the message to the server
        socket.emit('message', message);
        // Clear the message input after sending
        setMessage('');
    };

    return (
        <div>
            <h1>Chat Room</h1>
            <div>
                {/*Map over the messages array to render messages */}
                {messages.map((msg, index) => (
                    <p key={index}>{msg}</p> // Use index as key for simplicity (ideally, messages should have unique ids)
                ))}
            </div>
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)} // Update message state on every input change
            />
            <button onClick={sendMessage}>Send</button> // Trigger sendMessage on click
        </div>
    );
}

export default Chat;