import discord 
from discord import app_commands

id_server = discord.Object(id=1341783606078734389)

class clientsCommand(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self):
        self.tree.copy_global_to(guild=id_server)
        
        await self.tree.sync(guild=id_server)
        
client = clientsCommand()

@client.tree.command(name="chat", description="Chat or ask me anything!")
@app_commands.describe(prompt="Answer the client's question")
async def chat(interaction: discord.Interaction, prompt:str):
    await interaction.response.send_message(f"Wait a moment, please. I'm figuring about: {prompt}")