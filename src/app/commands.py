import asyncio
import discord 
import os
from dotenv import load_dotenv
from discord import app_commands
from google import genai

load_dotenv()

serverCreds = os.getenv('server_credential')  # This variable contains my server ID and i store it in .env
myGuild = discord.Object(id=int(serverCreds))
llmCreds = os.getenv('llm_credential')

class clientsCommand(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self):
        self.tree.copy_global_to(guild=myGuild)
        await self.tree.sync(guild=myGuild)
        
client = clientsCommand()
ai_client = genai.Client(api_key=llmCreds)

# First chatbot command, /chat. use this comm to ask or chat with AI.
@client.tree.command(name="chat", description="Chat or ask me anything!")
@app_commands.describe(prompt="Answer the client's question")

async def chat(interaction: discord.Interaction, prompt:str):
    await interaction.response.defer()
    
    max_retries = 3
    retry_delay = 3
    
    for attempt in range(max_retries):
        try:
            response = ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )

            await interaction.followup.send(response.text)
            return

        except Exception as e:
            if "503" in str(e) and attempt < max_retries - 1 :
                print(f"Server busy (Attempt to retry {attempt + 1}/{max_retries}. Retrying in {retry_delay} seconds...)")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2
            else:
                print(f"Gemini error after final attempt {e}")
                await interaction.followup.send("Server is recently busy, let's try again after a moment!")
                return