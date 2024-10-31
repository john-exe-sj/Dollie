import discord
from discord.ext import commands
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import os
import re
import logging

# Configuring basic logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()

DOLLIE_REGEX = re.compile(r'\b[dD]ollie\b')

# Initializing llm 
llm = OllamaLLM(model=os.getenv('MODEL_NAME'))

# Create a bot instance with a command prefix
intents = discord.Intents.all() 
bot = commands.Bot(command_prefix=os.getenv('APP_COMMAND_PREFIX'),intents=intents)

# Event when the bot is ready
@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name} - {bot.user.id}')

@bot.event
async def on_message(message):
    # Prevent the bot from responding to its own messages
    if message.author == bot.user:
        return

    # Check if the message is a command
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)  # Process commands
    
    # detects if dollie is being called upon to act. 
    if DOLLIE_REGEX.search(message.content):

        # TODO: Create a messaging FIFO Queue, Dollie so far cannot process multiple requests
        # from various users or multiple requests from the same user. 

        # notifies user that dollie is thinking
        usr_id = f"<@{message.author.id}>"
        await message.channel.send(f"Thinking... {usr_id}, I will mention you when I finish the task.")
        # take out the name dollie from request payload, llm is not actually 'dollie'. 
        payload = DOLLIE_REGEX.sub("", message.content) 
        response = llm.invoke(payload) # send the payload to the llm for processing. 

        if response:
            # include the user_id for mentions once the request/payload has been processed. 
            await message.channel.send(usr_id + ": " + response) 
        else:
            await message.channel.send("I couldn't generate a response.")

    
@bot.command()
@commands.has_permissions(administrator=True)  # Only users with administrator permissions can use this command
async def shutdown(ctx):
    logger.info(f'Shutting down... {bot.user.name} - {bot.user.id}')
    await ctx.send("Shutting down...")
    await bot.close()  # Logs the bot out

# Error handling for missing permissions
@shutdown.error
async def shutdown_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        logger.error(f'ERROR: Shutting down with improper permissions {bot.user.name} - {bot.user.id}')
        await ctx.send("You do not have permission to use this command.")


def run_bot():
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not DISCORD_BOT_TOKEN:
        raise ValueError("DISCORD_BOT_TOKEN environment variable not set.")
    else: 
        bot.run(DISCORD_BOT_TOKEN) 
