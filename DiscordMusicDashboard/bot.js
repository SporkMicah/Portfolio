// bot.js

// Load environment variables from .env file for secure access to tokens
require('dotenv').config();

// Import necessary libraries from discord.js and other dependencies
const { Client, GatewayIntentBits } = require('discord.js');
const { joinVoiceChannel, createAudioResource, createAudioPlayer, AudioPlayerStatus } = require('@discordjs/voice');
const ytdl = require('ytdl-core');

// Create new discord client instance with necessary intents to handle guilds and messages
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildVoiceStates,
    ]
});

// Handles music playback in a voice channel
class MusicPlayer {
    constructor() {
        this.connection = null;
        this.player = null;
    }

    async play(url, voiceChannel) {
        if (!ytdl.validateURL(url)) {
            return 'Please provide a valid YouTube URL.';
        }

        // Join the voice channel only if not already connected
        if (!this.connection) {
            this.connection = joinVoiceChannel({
                channelId: voiceChannel.id,
                guildId: voiceChannel.guild.id,
                adapterCreator: voiceChannel.guild.voiceAdapterCreator,
            });
        }

        const stream = ytdl(url, { filter: 'audioonly' });
        const resource = createAudioResource(stream);
        this.player = createAudioPlayer();
        this.player.play(resource);
        this.connection.subscribe(this.player);

        this.player.on(AudioPlayerStatus.Idle, () => {
            this.connection.destroy();
            this.connection = null;
        });

        return `Now playing: ${url}`;
    }
}

const musicPlayer = new MusicPlayer();

// Event listener for when the bot is ready
client.once('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

// Event listener for message creation to handle commands
client.on('messageCreate', async message => {
    if (message.author.bot || !message.content.startsWith('!play')) return;

    const args = message.content.split(' ');
    const url = args[1];
    if (!url) {
        message.channel.send('Please provide a YouTube URL.');
        return;
    }

    const voiceChannel = message.member.voice.channel;
    if (!voiceChannel) {
        message.channel.send('You need to be in a voice channel to play music.');
        return;
    }

    const response = await musicPlayer.play(url, voiceChannel);
    message.channel.send(response);
});

// Log the bot in using the token from the .env file
client.login(process.env.DISCORD_TOKEN);
