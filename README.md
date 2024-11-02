# Dollie Discord Bot

Dollie is a Discord bot built using `discord.py` and `langchain_ollama`. It processes user messages asynchronously and interacts with an AI model to generate responses.

## Features

- Responds to messages mentioning "Dollie".
- Processes messages in a queue to handle multiple requests efficiently.
- Supports command-based interactions.
- Graceful shutdown command for administrators.

## Potential Upcoming Features:
- Capability to mention and process files (images/pdf) to generate responses. 
- Short-term context for conversations.
- Ability to respond to messages in threads. 

## Requirements

- Python 3.7 or higher
- `discord.py`
- `langchain_ollama`
- `python-dotenv`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/dollie-discord-bot.git
   cd dollie-discord-bot
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add the following environment variables:

   ```plaintext
   DISCORD_BOT_TOKEN=your_discord_bot_token
   MODEL_NAME=your_model_name
   APP_COMMAND_PREFIX=your_command_prefix
   ```

   Replace `your_discord_bot_token`, `your_model_name`, and `your_command_prefix` with your actual values.

## Usage

1. Run the bot:

   ```bash
   python src/DollieModule.py
   ```

2. Invite the bot to your Discord server using the OAuth2 URL generated in the Discord Developer Portal.

3. Interact with the bot by mentioning "Dollie" in any channel where the bot has access.

## Commands

- `!shutdown`: Shuts down the bot (admin only). NOTE: command prefix is configurable and should be included in your .env file. 

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

No licensing is available for this project. It is free for public use.

## Acknowledgments

- [discord.py](https://discordpy.readthedocs.io/en/stable/) - The library used to interact with the Discord API.
- [langchain_ollama](https://github.com/yourusername/langchain_ollama) - The AI model integration.
