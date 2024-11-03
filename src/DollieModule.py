import discord
from discord.ext import commands
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import asyncio
import os
import re
import logging

# Create a bot instance with a command prefix
intents = discord.Intents.all() 
bot = commands.Bot(command_prefix=os.getenv('APP_COMMAND_PREFIX'), intents=intents)

# Configuring basic logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# regular expression to account for different variations of how to refer to dollie, even in leetspeak. 
DOLLIE_REGEX = re.compile(r'\b[dD][o0][l1|][l1|][i1!][e3]?\b', re.IGNORECASE)

# Initializing llm 
llm = OllamaLLM(model=os.getenv('MODEL_NAME'))

# Create an asyncio Queue
request_queue = asyncio.Queue()

async def process_messages(): 
    while True: 
        usr_id, payload, message = await request_queue.get()  # Wait for a message to be available
        try:
            response = await llm.ainvoke(payload)  # Send the payload to the LLM for processing
            if response:
                await message.channel.send(f"{usr_id}: {response}") 
            else:
                await message.channel.send("I couldn't generate a response.") 
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await message.channel.send("An error occurred while processing your request.")
        finally:
            request_queue.task_done()

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name} - {bot.user.id}')
    bot.loop.create_task(process_messages())  # Start processing messages

@bot.event
async def on_message(message):
    # Prevent the bot from responding to its own messages
    if message.author == bot.user:
        return

    # Check if the message is a command
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)  # Process commands
    
    # detects if dollie is being called upon to act. 
    if DOLLIE_REGEX.search(message.content) or f'<@{bot.user.id}>' in message.content:

        usr_id = f"<@{message.author.id}>"
        payload = None
        if DOLLIE_REGEX.search(message.content): 
            payload = DOLLIE_REGEX.sub("", message.content)
        else: 
            payload = message.content.replace(f'<@{bot.user.id}>', "")
        
        # queues in user's request. 
        await request_queue.put((usr_id, payload, message))
        # notifies user that dollie is thinking
        await message.channel.send(f"Thinking... {usr_id}, I will mention you when I finish the task.")
        logger.info(f"Recording {usr_id}'s request")

@bot.command()
@commands.has_permissions(administrator=True)  # Only users with administrator permissions can use this command
async def shutdown(ctx):
    logger.info(f'Shutting down... {bot.user.name} - {bot.user.id}')
    await ctx.send("Shutting down...")
    
    # Wait for the queue to be empty before shutting down
    await request_queue.join()  # Wait until all tasks are done
    await bot.close()  # Logs the bot out

# Error handling for missing permissions
@shutdown.error
async def shutdown_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        logger.error(f'ERROR: Shutting down with improper permissions {bot.user.name} - {bot.user.id}')
        await ctx.send("You do not have permission to use this command.")

def run_bot():
    # Run the bot
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not DISCORD_BOT_TOKEN:
        raise ValueError("DISCORD_BOT_TOKEN environment variable not set.")
    if not os.getenv('MODEL_NAME'):
        raise ValueError("MODEL_NAME environment variable not set.")
    if not os.getenv('APP_COMMAND_PREFIX'):
        raise ValueError("APP_COMMAND_PREFIX environment variable not set.")
    
    asyncio.run(bot.start(DISCORD_BOT_TOKEN))  # Use asyncio.run to start the bot