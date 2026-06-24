import discord 
import os
from dotenv import load_dotenv
from discord import app_commands
from src.handler.mention import handle_mention
from src.service.gemini_service import get_response
from src.components.chat import chat_response

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
        
    async def chat_response(self, message: discord.Message):
        await self.chat_response(self, message)
    
client = clientsCommand()

# First chatbot command, /chat. use this comm to ask or chat with AI.
# @client.tree.command(name="report_bug", description="If there's a bug, please submit a report form here")
# @app_commands.describe(prompt="Your prompt goes here")
# async def report_bug(interaction: discord.Interaction, bug_report: str):
#     """Handle bug reports from users"""
#     await interaction.response.send_message(f"Thank you for reporting: {bug_report}")

