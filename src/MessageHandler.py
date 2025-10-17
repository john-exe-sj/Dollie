from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.chat_history import BaseChatMessageHistory
from typing import List
from dotenv import load_dotenv
import discord
import os
import logging
import time
import asyncio
from .SecretsManager import get_secret

secret = get_secret()
load_dotenv()

# Configuring basic logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initializing LLM
llm = ChatGroq(
    groq_api_key=secret["DOLLIES_GROQ_KEY"],
    model_name=secret["MODEL_NAME"]
)

MAX_AMT_CHR_MSGS = 2000
MAX_AMT_CHR_EMBED = 4000

# Message history store with timestamps for cleanup
store = {}
store_timestamps = {}

# Custom message history store
class InMemoryChatMessageHistory(BaseChatMessageHistory):

    def __init__(self, system_message: str = ""):
        self.messages: List = []
        if system_message:
            self.messages.append(SystemMessage(content=system_message))

    def add_user_message(self, message: str) -> None:
        self.messages.append(HumanMessage(content=message))

    def add_ai_message(self, ai_message: AIMessage) -> None:
        self.messages.append(ai_message)

    def add_system_message(self, message: str) -> None:
        """Add a system message to the conversation"""
        self.messages.append(SystemMessage(content=message))

    def clear(self) -> None:
        self.messages.clear()

def get_session_history(user_id: str,
                        bot_client_id: str = "") -> BaseChatMessageHistory:
    if user_id not in store:
        # Create initial system message
        system_message = f"""You are a helpful chat-bot assistant with the user id; {bot_client_id} that strictly answers programming,
        computer science, data structures, algorithm or any computer-related questions for children who are ages 6 and older. 
        You must not include your user id in your responses. Keep the responses as simple as possible using terminology a child from
        ages 6 or older can understand. Keep in mind, you are a chat-bot assistant for children who are ages 6 or older, so do
        not include violence and profanity. Neither should you imply any violent acts or suggest things/actions that a child should do.
        You are not to mention this in your responses."""

        store[user_id] = InMemoryChatMessageHistory(
            system_message=system_message)
        store_timestamps[user_id] = time.time()
    else:
        # Update timestamp when session is accessed
        store_timestamps[user_id] = time.time()
    return store[user_id]

async def cleanup_old_sessions(max_age_hours: int = 24):
    """Remove sessions older than max_age_hours"""
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    to_remove = []

    for user_id, timestamp in store_timestamps.items():
        if current_time - timestamp > max_age_seconds:
            to_remove.append(user_id)

    for user_id in to_remove:
        del store[user_id]
        del store_timestamps[user_id]
        logger.info(f"Cleaned up old session: {user_id}")

    if to_remove:
        logger.info(f"Cleaned up {len(to_remove)} old sessions")

async def periodic_cleanup(interval_hours: int = 1):
    """Run cleanup periodically in the background"""
    while True:
        await asyncio.sleep(interval_hours * 3600)  # Convert hours to seconds
        await cleanup_old_sessions()

async def process_messages(request_queue):

    while True:
        usr_id, payload, message, bot_user = await request_queue.get(
        )  # Wait for a message to be available
        try:
            # Get the session history for this user
            session_history = get_session_history(usr_id, str(bot_user))

            # TODO: Add further contextual information by use of a vectordb.
            # - Store it as a system message.

            # Add the user's message to history
            session_history.add_user_message(payload)

            # Get all messages from history (including system message)
            all_messages = session_history.messages

            # Get response from LLM, recieved as an AIMessage() object.
            response = await llm.ainvoke(all_messages)

            # Add AI response to history
            session_history.add_ai_message(response)
            if response:  # Check if response is not empty
                response_length = len(
                    response.content)  # Get the length of the response
                logging.info(f"Response length: {response_length}"
                             )  # Log the length of the response

                if response_length < MAX_AMT_CHR_MSGS:
                    await message.channel.send(f"{usr_id}: {response.content}")
                elif response_length < MAX_AMT_CHR_EMBED:
                    embed = discord.Embed(description=response.content)
                    await message.channel.send(
                        f"{usr_id}, here's my response, it's longer than usual.",
                        embed=embed)
                else:  # Response is too long
                    # Create the directory if it doesn't exist
                    os.makedirs(
                        "../output",
                        exist_ok=True)  # Use exist_ok to avoid checking

                    # Write response to a file
                    file_path = '../output/response.txt'
                    with open(file_path, 'w') as file:
                        logger.info(f"Creating/Writing text file {file_path}")
                        file.write(response.content)
                    await message.channel.send(
                        f"{usr_id}, here's my response as a text file",
                        file=discord.File(file_path))
            else:  # No response
                await message.channel.send(
                    f"{usr_id}: Could not send message. We've reached the limitations of Discord."
                )

        except Exception as e:
            logger.error(f"Error processing message: {e}, {e.args}")
            await message.channel.send(
                "An error occurred while processing your request.")
        finally:
            request_queue.task_done()
