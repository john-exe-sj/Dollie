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

# Regular expression to account for different variations of how to refer to Dollie
DOLLIE_REGEX = re.compile(r'\b[dD][o0][l1|][l1|][i1!][e3]?\b', re.IGNORECASE)
# Initializing LLM 
llm = OllamaLLM(model=os.getenv('MODEL_NAME'))

# Create a request queue via asyncio. This is how we keep track on who to serve next. 
request_queue = asyncio.Queue()

MAX_AMT_CHR_MSGS = 2000
MAX_AMT_CHR_EMBED = 4000

async def process_messages(): 
    while True: 
        usr_id, payload, message = await request_queue.get()  # Wait for a message to be available
        try:
            response = await llm.ainvoke(payload)  # Send the payload to the LLM for processing

            if response:  # Check if response is not empty
                if len(response) < MAX_AMT_CHR_MSGS:
                    await message.channel.send(f"{usr_id}: {response}")
                elif len(response) < MAX_AMT_CHR_EMBED:
                    embed = discord.Embed(description=response)
                    await message.channel.send(
                        f"{usr_id}, here's my response, it's longer than usual.", 
                        embed=embed
                    )
                else:  # Response is too long
                    # Create the directory if it doesn't exist
                    os.makedirs("../output", exist_ok=True)  # Use exist_ok to avoid checking

                    # Write response to a file
                    file_path = '../output/response.txt'
                    with open(file_path, 'w') as file:
                        file.write(response)
                    await message.channel.send(
                        f"{usr_id}, here's my response as a text file", 
                        file=discord.File(file_path)
                    )
            else:  # No response
                await message.channel.send(f"{usr_id}: Could not send message. We've reached the limitations of Discord.")
                 
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

    bot_member = message.guild.me  # Get the bot's member object in the guild
    role_ids = [role.id for role in bot_member.roles if role.name != "@everyone"]  # Get the roles

    # Check if Dollie is being called upon to act
    was_mentioned_via_role = any(f'<@&{role_id}>' in message.content for role_id in role_ids)

    if DOLLIE_REGEX.search(message.content) or f'<@{bot.user.id}>' in message.content or was_mentioned_via_role:
        usr_id = f"<@{message.author.id}>"
        payload = DOLLIE_REGEX.sub("", message.content) if DOLLIE_REGEX.search(message.content) else message.content
        payload = payload.replace(f'<@{bot.user.id}>', "")  # Remove bot mention
        
        # Remove any role mentions
        for role_id in role_ids:
            payload = payload.replace(f'<@&{role_id}>', "")
        
        # Queue the user's request
        await request_queue.put((usr_id, payload, message))
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