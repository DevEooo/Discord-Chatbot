import discord 
import os
from dotenv import load_dotenv
from discord import app_commands
from src.handler.mention import handle_mention
from src.service.gemini_service import get_response

load_dotenv()

serverCreds = os.getenv('server_credential')  # This variable contains my server ID and i store it in .env
myGuild = discord.Object(id=int(serverCreds))

class clientsCommand(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True 
        
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self):
        self.tree.copy_global_to(guild=myGuild)
        await self.tree.sync(guild=myGuild)
        
    async def on_message(self, message: discord.Message):
        await handle_mention(self, message)
    
client = clientsCommand()

# First chatbot command, /chat. use this comm to ask or chat with AI.
@client.tree.command(name="chat", description="Chat or ask me anything!")
@app_commands.describe(prompt="Your prompt goes here")

async def chat(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    chunks = await get_response(prompt)

    await interaction.followup.send(chunks[0])
    
    for chunk in chunks[1:]:
        await interaction.channel.send(chunk)
    
