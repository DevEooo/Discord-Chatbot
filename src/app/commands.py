import discord 
import os
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()

serverCreds = os.getenv('server_credential')  # This variable contains my server ID and i store it in .env

myGuild = discord.Object(id=int(serverCreds))

class clientsCommand(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self):
        self.tree.copy_global_to(guild=myGuild)
        
        await self.tree.sync(guild=myGuild)
        
client = clientsCommand()

@client.tree.command(name="chat", description="Chat or ask me anything!")
@app_commands.describe(prompt="Answer the client's question")

async def chat(interaction: discord.Interaction, prompt:str):
    await interaction.response.send_message(f"Wait a moment, please. I'm figuring about: {prompt}")