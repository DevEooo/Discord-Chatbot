import discord, os
from discord import app_commands
from src.handler.mention import handle_mention
from src.handler.bug_report import BugReportModal

serverCreds = os.getenv('server_credential')  # This variable contains my server ID and i store it in .env
if not serverCreds:
    raise ValueError("[ERROR]: 'server_credential' is missing in .env")

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
