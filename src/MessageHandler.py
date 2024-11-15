from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import discord
import os
import logging

load_dotenv()

# Configuring basic logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initializing LLM 
llm = OllamaLLM(model=os.getenv('MODEL_NAME'))

MAX_AMT_CHR_MSGS = 2000
MAX_AMT_CHR_EMBED = 4000

async def process_messages(request_queue): 
    while True: 
        usr_id, payload, message = await request_queue.get()  # Wait for a message to be available
        try:
            print(payload)
            response = await llm.ainvoke(payload)  # Send the payload to the LLM for processing
            
            if response:  # Check if response is not empty
                response_length = len(response)  # Get the length of the response
                logging.info(f"Response length: {response_length}")  # Log the length of the response

                if response_length < MAX_AMT_CHR_MSGS:
                    await message.channel.send(f"{usr_id}: {response}")
                elif response_length < MAX_AMT_CHR_EMBED:
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
                        logger.info(f"Creating/Writing text file {file_path}")
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
