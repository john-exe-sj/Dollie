import discord
from discord.ext import commands
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import os
import re
import random

load_dotenv()

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
    if "dollie" in message.content.lower():
        
        message.content = re.sub("\b[dD]ollie\b", "", message.content)

        notifying_strings = [
            "Got it, let me work that out for you.", 
            "Let me see what I can do.", 
            "Let me cook!", 
            "Loud and clear, I'm sure I can come up with something for you. Sit tight.", 
        ]

        await message.channel.send(random.choice(notifying_strings))
        
        if type(message.content) == str:
            response = llm.invoke(message.content)
            await message.channel.send(response)


    
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
