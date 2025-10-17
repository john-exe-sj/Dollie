# Dollie Discord Bot 🤖

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.3+-green.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-Free-red.svg)]()

Dollie is an intelligent Discord bot built using `discord.py` and `langchain-groq`. It processes user messages asynchronously and provides AI-powered responses through Groq's language models, specifically designed to help children aged 6+ with programming and computer science questions.

## ✨ Features

### Core Functionality
- **Smart Message Detection**: Responds to messages mentioning "Dollie" or through role and direct mentions
- **Asynchronous Processing**: Handles multiple requests efficiently using a message queue system
- **Session Management**: Maintains conversation history per user with automatic cleanup
- **Child-Friendly AI**: Specifically designed responses for children ages 6 and older
- **Command Support**: Built-in command system with configurable prefix

### Advanced Features
- **Intelligent Response Handling**: Automatically handles responses of varying lengths
  - Short responses: Direct message
  - Medium responses: Discord embeds
  - Long responses: File attachments
- **Role-Based Mentions**: Responds to both direct mentions and role mentions
- **Channel Restrictions**: Configurable channel access control
- **Graceful Shutdown**: Admin-only shutdown command with queue completion
- **Periodic Cleanup**: Automatic session cleanup to manage memory usage

## 🚀 Upcoming Features

- **File Processing**: Support for images and PDFs
- **Enhanced Context Management**:
  - Vector database for semantic context retrieval
  - Sliding window conversation history
  - Advanced token counting and management
  - Persistent storage for conversation history
- **Thread Support**: Ability to respond in Discord threads
- **Multi-Model Support**: Support for different AI models beyond Groq 

## 📋 Requirements

- **Python**: 3.7 or higher
- **Discord.py**: 2.3.0 or higher
- **LangChain Groq**: For AI model integration
- **Python-dotenv**: For environment variable management

## 🛠️ Installation

### Prerequisites
- A Discord application and bot token
- A Groq API key (free tier available)
- Python 3.7+ (for local installation) or Docker (for containerized deployment)

### Option 1: Local Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/dollie-discord-bot.git
   cd dollie-discord-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   
   Create a `.env` file in the root directory:
   ```env
   # Discord Bot Configuration
   DISCORD_BOT_TOKEN=your_discord_bot_token
   APP_COMMAND_PREFIX=!
   
   # AI Model Configuration
   MODEL_NAME=llama-3.1-8b-instant
   DOLLIES_GROQ_KEY=your_groq_api_key
   
   # Channel Configuration
   LIST_OF_ACCEPTABLE_CHANNELS=channel_id_1,channel_id_2
   ```

### Option 2: Docker Deployment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/dollie-discord-bot.git
   cd dollie-discord-bot
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

3. **Run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

4. **Or build and run manually**:
   ```bash
   # Build the image
   docker build -t dollie-bot .
   
   # Run the container
   docker run -d \
     --name dollie-discord-bot \
     --env-file .env \
     -v $(pwd)/output:/app/output \
     dollie-bot
   ```

### Environment Variables

**Required Variables**:
- `DISCORD_BOT_TOKEN`: Your Discord bot token from the Discord Developer Portal
- `MODEL_NAME`: Groq model name (e.g., `llama-3.1-8b-instant`, `mixtral-8x7b-32768`)
- `DOLLIES_GROQ_KEY`: Your Groq API key from [console.groq.com](https://console.groq.com)
- `APP_COMMAND_PREFIX`: Command prefix for bot commands (default: `!`)
- `LIST_OF_ACCEPTABLE_CHANNELS`: Comma-separated list of channel IDs where the bot can respond

## 🚀 Usage

### Starting the Bot

1. **Run the bot**:
   ```bash
   python main.py
   ```

2. **Invite to Discord server**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Select your application
   - Navigate to OAuth2 > URL Generator
   - Select `bot` scope and necessary permissions
   - Use the generated URL to invite the bot to your server

3. **Interact with Dollie**:
   - Mention "Dollie" in any allowed channel
   - Use direct mentions: `@Dollie your question here`
   - Use role mentions if the bot has roles assigned
   - The bot will respond with child-friendly programming and computer science explanations

## 🎮 Commands

| Command | Description | Permission Required |
|---------|-------------|-------------------|
| `!shutdown` | Gracefully shuts down the bot after completing all queued requests | Administrator |

> **Note**: The command prefix is configurable via the `APP_COMMAND_PREFIX` environment variable.

## 🔧 Configuration

### Discord Bot Permissions
Ensure your bot has the following permissions:
- **Send Messages**
- **Read Message History**
- **Use Slash Commands** (if using slash commands)
- **Embed Links** (for longer responses)

### Supported Groq Models
- `llama-3.1-8b-instant` (recommended for fast responses)
- `llama-3.1-70b-versatile` (for more complex queries)
- `mixtral-8x7b-32768` (balanced performance)
- `gemma-7b-it` (alternative option) 

## 🐛 Troubleshooting

### Common Issues

**Bot not responding**:
- Verify the bot token is correct
- Check that the channel ID is in `LIST_OF_ACCEPTABLE_CHANNELS`
- Ensure the bot has proper permissions in the channel

**API errors**:
- Verify your Groq API key is valid
- Check if you've exceeded rate limits
- Ensure the model name is correct

**Session cleanup issues**:
- Sessions automatically clean up after 24 hours of inactivity
- Manual cleanup runs every hour in the background

### Docker Issues

**Container won't start**:
- Check if all environment variables are set correctly
- Verify the `.env` file exists and has proper values
- Check container logs: `docker logs dollie-discord-bot`

**Permission issues**:
- Ensure the output directory has proper permissions
- The container runs as a non-root user for security

**Build failures**:
- Clear Docker cache: `docker system prune -a`
- Rebuild without cache: `docker build --no-cache -t dollie-bot .`

**Docker Compose issues**:
- Check if ports are already in use
- Verify the compose file syntax: `docker-compose config`

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Issues**: Found a bug? Open an issue with detailed information
2. **Feature Requests**: Have an idea? Submit a feature request
3. **Code Contributions**: Fork the repo and submit a pull request
4. **Documentation**: Help improve this README or add code comments

### Development Setup
```bash
# Clone and setup
git clone https://github.com/yourusername/dollie-discord-bot.git
cd dollie-discord-bot
pip install -r requirements.txt

# Create development environment
cp .env.example .env
# Edit .env with your configuration
```

## 📄 License

This project is free for public use. No licensing restrictions apply.

## 🙏 Acknowledgments

- **[discord.py](https://discordpy.readthedocs.io/en/stable/)** - Discord API wrapper for Python
- **[LangChain](https://langchain.com/)** - Framework for building LLM applications
- **[Groq](https://groq.com/)** - Fast AI inference platform
- **[LangChain Groq](https://python.langchain.com/docs/integrations/chat/groq)** - Groq integration for LangChain

---

**Made with ❤️ for helping kids learn programming and computer science!**
