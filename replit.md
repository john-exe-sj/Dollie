# Dollie Discord Bot

## Overview
Dollie is a Discord bot that uses AI (Groq's language models via LangChain) to answer programming and computer science questions for children ages 6 and older. The bot processes user messages asynchronously using a queue system and maintains conversation history for each user.

**Current Status**: Fully configured and running on Replit
**Last Updated**: October 10, 2025

## Project Architecture

### Structure
```
.
├── main.py                 # Main bot entry point, handles Discord events
├── src/
│   ├── __init__.py
│   └── MessageHandler.py   # Message processing logic and AI integration
├── requirements.txt        # Python dependencies
└── README.md              # Original project documentation
```

### Key Features
- Responds to messages mentioning "Dollie" or through role/direct mentions
- Processes messages in a queue to handle multiple requests efficiently
- Maintains per-user conversation history with automatic cleanup (24-hour expiry)
- Supports command-based interactions (e.g., shutdown command)
- Graceful handling of long responses (uses embeds or files for longer messages)

### Technology Stack
- **Language**: Python 3.11
- **Discord API**: discord.py >= 2.3.0
- **AI Integration**: LangChain + Groq API (langchain-groq)
- **Environment**: Replit (NixOS)

## Configuration

### Required Environment Variables
All secrets are stored in Replit Secrets:

1. **DISCORD_BOT_TOKEN** - Discord bot authentication token
2. **DOLLIES_GROQ_KEY** - Groq API key for AI functionality
3. **MODEL_NAME** - Groq AI model name (e.g., "llama-3.3-70b-versatile")
4. **APP_COMMAND_PREFIX** - Bot command prefix (e.g., "!")
5. **LIST_OF_ACCEPTABLE_CHANNELS** - Comma-separated Discord channel IDs

### Workflow
- **Name**: Discord Bot
- **Command**: `python main.py`
- **Type**: Console application (runs continuously)

## How It Works

### Message Flow
1. User mentions "Dollie" (or variations) or uses @mention
2. Message is added to an async queue
3. Bot acknowledges with "Thinking..." message
4. AI processes the message using conversation history
5. Response is sent (as text, embed, or file depending on length)
6. Conversation history is updated

### Session Management
- Each user has their own conversation history
- Sessions expire after 24 hours of inactivity
- Periodic cleanup runs every hour
- System message defines bot personality and constraints

### Admin Commands
- `!shutdown` (or custom prefix + shutdown): Gracefully shuts down the bot
  - Only users with administrator permissions can use this
  - Waits for queue to finish processing before shutting down

## Development Notes

### Dependencies
All dependencies are managed via pip and requirements.txt:
- discord.py: Discord API wrapper
- langchain-groq: Groq AI integration
- langchain & langchain-core: LangChain framework
- python-dotenv: Environment variable management

### Code Conventions
- Uses async/await for Discord event handling
- Implements queue-based message processing for concurrency
- Logging configured at INFO level
- Error handling for permission issues and API failures

## Recent Changes
- **Oct 10, 2025**: Initial Replit setup and configuration
  - Installed Python 3.11 and all dependencies
  - Configured environment secrets
  - Set up Discord Bot workflow
  - Verified bot successfully connects and runs

## User Preferences
(None specified yet)
