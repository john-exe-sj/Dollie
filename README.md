# Dollie Discord Bot 🤖

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.3+-green.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-Free-red.svg)]()

Dollie is an intelligent Discord bot built using `discord.py` and `langchain-anthropic`. Hosted on Amazon Web Services, it processes user messages asynchronously and provides AI-powered responses through Anthropic's Claude models, specifically designed to help children aged 6+ with programming and computer science questions.

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
- **Multi-Model Support**: Configure the Claude model through `MODEL_NAME`

## 📋 Requirements

- **Python**: 3.7 or higher
- **Discord.py**: 2.3.0 or higher
- **LangChain Anthropic**: For Claude model integration
- **Anthropic API key**: Store as `DOLLIES_ANTHROPIC_KEY` in the application secrets
- **Model name**: Set `MODEL_NAME` to a supported Claude model ID (Docker Compose defaults to `claude-sonnet-4-5`)
- **Python-dotenv**: For environment variable management

## 🚀 Usage

1. **Interact with Dollie**:

- Mention "Dollie" in any allowed channel
- Use direct mentions: `@Dollie your question here`
- Use role mentions if the bot has roles assigned
- The bot will respond with child-friendly programming and computer science explanations

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Issues**: Found a bug? Open an issue with detailed information
2. **Feature Requests**: Have an idea? Submit a feature request
3. **Code Contributions**: Fork the repo and submit a pull request
4. **Documentation**: Help improve this README or add code comments

### 📄 License

This project is free for public use. No licensing restrictions apply.

## 🙏 Acknowledgments

- **[discord.py](https://discordpy.readthedocs.io/en/stable/)** - Discord API wrapper for Python
- **[LangChain](https://langchain.com/)** - Framework for building LLM applications
- **[Anthropic](https://www.anthropic.com/)** - Claude models
- **[LangChain Anthropic](https://python.langchain.com/docs/integrations/chat/anthropic/)** - Anthropic integration for LangChain
- **[Amazon Web Services](https://aws.amazon.com/)** - EC2 Instance hosting and logging.

---

**Made with ❤️ for helping kids learn programming and computer science!**
