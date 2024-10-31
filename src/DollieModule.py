import discord
from discord.ext import commands
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import os
import re

load_dotenv()

DOLLIE_REGEX = re.compile(r'\b[db]ollie\b')

# Initializing llm 
llm = OllamaLLM(model=os.getenv('MODEL_NAME'))

# Create a bot instance with a command prefix
intents = discord.Intents.all() 
bot = commands.Bot(command_prefix='.',intents=intents)

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

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

        # notifies user that dollie is thinking
        usr_id = f"<@{message.author.id}>:\n"
        await message.channel.send(f"Thinking... {usr_id}, I will mention you when I finish the task.")
        payload = DOLLIE_REGEX.sub("", message.content)
        response = llm.invoke(payload)
        if response:
            await message.channel.send(usr_id + response)
        else:
            await message.channel.send("I couldn't generate a response.")
        


    
@bot.command()
@commands.has_permissions(administrator=True)  # Only users with administrator permissions can use this command
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    await bot.close()  # Logs the bot out

# Error handling for missing permissions
@shutdown.error
async def shutdown_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")


def run_bot():
    bot_token = os.getenv('DISCORD_BOT_TOKEN')
    bot.run(bot_token) 
