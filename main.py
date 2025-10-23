from discord.ext import commands
from src.MessageHandler import process_messages, periodic_cleanup
import discord
import asyncio
import re
import logging
import watchtower
from src.SecretsManager import get_secret

# Obtaining secrets from AWS Secrets Manager
secrets = get_secret()

# Configuring basic logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cw_handler = watchtower.CloudWatchLogHandler(log_group=secrets['CLOUD_WATCH_LOG_GROUP'])
# Add the CloudWatch handler to the logger
logger.addHandler(cw_handler)

# Create a bot instance with a command prefix
intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=secrets['APP_COMMAND_PREFIX'],
    intents=intents
)

# Regular expression to account for different variations of how to refer to Dollie
DOLLIE_REGEX = re.compile(r'\b[dD][o0][l1|][l1|][i1!][e3]?\b', re.IGNORECASE)

# Create a request queue via asyncio. This is how we keep track on who to serve next.
request_queue = asyncio.Queue()

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name} - {bot.user.id}')
    bot.loop.create_task(
        process_messages(request_queue))  # Start processing messages
    bot.loop.create_task(periodic_cleanup())  # Start periodic cleanup task

@bot.event
async def on_message(message):
    # Prevent the bot from responding to its own messages
    if message.author == bot.user:
        return

    # Check if the message is in the allowed channel
    if str(message.channel.id) not in secrets['LIST_OF_ACCEPTABLE_CHANNELS'].split(","):
        logger.info(f"Message not in allowed channel {message.channel.id}")
        return

    # Check if the message is a command
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)  # Process commands

    bot_member = message.guild.me  # Get the bot's member object in the guild
    role_ids = [
        role.id for role in bot_member.roles if role.name != "@everyone"
    ]  # Get the roles

    # Check if Dollie is being called upon to act
    was_mentioned_via_role = any(f'<@&{role_id}>' in message.content
                                 for role_id in role_ids)

    if DOLLIE_REGEX.search(
            message.content
    ) or f'<@{bot.user.id}>' in message.content or was_mentioned_via_role:
        usr_id = f"<@{message.author.id}>"
        payload = DOLLIE_REGEX.sub("", message.content) if DOLLIE_REGEX.search(
            message.content) else message.content
        payload = payload.replace(f'<@{bot.user.id}>',
                                  "")  # Remove bot mention

        # Remove any role mentions
        for role_id in role_ids:
            payload = payload.replace(f'<@&{role_id}>', "")

        # Queue the user's request
        await request_queue.put((usr_id, payload, message, bot.user))
        logger.info(f"Recording {usr_id}'s request")

@bot.command()
@commands.has_permissions(
    administrator=True
)  # Only users with administrator permissions can use this command
async def shutdown(ctx):
    logger.info(f'Shutting down... {bot.user.name} - {bot.user.id}')
    logging.shutdown()
    
    await ctx.send("Shutting down...")

    # Wait for the queue to be empty before shutting down
    await request_queue.join()  # Wait until all tasks are done
    await bot.close()  # Logs the bot out

# Error handling for missing permissions
@shutdown.error
async def shutdown_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        logger.error(
            f'ERROR: Shutting down with improper permissions {bot.user.name} - {bot.user.id}'
        )
        await ctx.send("You do not have permission to use this command.")

def run_bot():
    # Run the bot
    if not secrets:
        raise ValueError("Could not retrieve AWS Secrets.")
    if not secrets['DISCORD_BOT_TOKEN']:
        raise ValueError("DISCORD_BOT_TOKEN environment variable not set.")
    if not secrets['MODEL_NAME']:
        raise ValueError("MODEL_NAME environment variable not set.")
    if not secrets['APP_COMMAND_PREFIX']:
        raise ValueError("APP_COMMAND_PREFIX environment variable not set.")

    asyncio.run(bot.start(secrets['DISCORD_BOT_TOKEN']))

if __name__ == "__main__":
    run_bot()
