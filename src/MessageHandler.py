from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from typing import List
from dotenv import load_dotenv
import discord
import os
import logging

load_dotenv()

# Configuring basic logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initializing LLM 
prompt_template = PromptTemplate.from_template(
    """
    You are a helpful chat-bot assistant with the user id; {bot_client_id} that strictly answers programming,
    computer science, data structures, algorithm or any computer-related questions for children who are ages 6 and older. 
    You must not include your user id in your responses. Keep the responses as simple as possible using terminology a child from
    ages 6 and older can understand. Keep in mind, you are a chat-bot assistant for children who are ages 6 and older, so do
    not include violence and profanity. Neither should you imply any violent acts or suggest things/actions that a child should do.
    You are not to mention this in your responses. 

    Given the following context; 
    {context}
    
    Answer or respond to the following; 
    {payload}
    """
)

llm = OllamaLLM(model=os.getenv('MODEL_NAME'))

MAX_AMT_CHR_MSGS = 2000
MAX_AMT_CHR_EMBED = 4000

context_map = {}

async def process_messages(request_queue): 

    while True: 
        usr_id, payload, message, bot_user = await request_queue.get()  # Wait for a message to be available
        try:

            if usr_id not in context_map:
                context_map[usr_id] = ""
            context = context_map[usr_id]

            # Format the prompt with the input variables
            formatted_prompt = prompt_template.format(
                bot_client_id=bot_user,
                context=context,
                payload=payload
            )

            # Invoke the LLM with the formatted prompt
            response = await llm.ainvoke(formatted_prompt)
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
                context_map[usr_id] += f"{usr_id}: {payload} \n{bot_user}: {response}"
            else:  # No response
                await message.channel.send(f"{usr_id}: Could not send message. We've reached the limitations of Discord.")
                 
        except Exception as e:
            logger.error(f"Error processing message: {e}, {e.args}")
            await message.channel.send("An error occurred while processing your request.")
        finally:
            request_queue.task_done()
