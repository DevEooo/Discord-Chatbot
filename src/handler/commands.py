import discord, os
from discord import app_commands
from src.handler.mention import handle_mention
from src.handler.report_bug import ReportBugModal

serverCreds = os.getenv('server_credential')  # This variable contains my server ID and i store it in .env
if not serverCreds:
    raise ValueError("[ERROR]: 'server_credential' is missing in .env")

myServer = discord.Object(id=int(serverCreds))

@app_commands.command(name="bug_report", description="Report a bug report directly to devs.")
@app_commands.checks.cooldown(1, 60.0, key=lambda i: i.user.id)
async def report_bug_command(interaction: discord.Interaction, attachment: discord.Attachment = None):
    await interaction.response.send_modal(ReportBugModal(attachment=attachment))

@report_bug_command.error
async def report_bug_error(interaction: discord.Interaction, e: app_commands.AppCommandError):
    if isinstance(e, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"On cooldown. Wait {e.retry_after:.1f}s before trying again.", ephemeral=True)

class clientsCommand(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True 
        
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self):
        self.tree.add_command(report_bug_command)
        await self.tree.sync()
        
        self.tree.copy_global_to(guild=myServer)
        await self.tree.sync(guild=myServer)
        
    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        await handle_mention(self, message)
        
client = clientsCommand()
    
