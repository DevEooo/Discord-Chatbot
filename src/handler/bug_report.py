import os, discord
from discord import app_commands

class BugReportModal(discord.ui.modal, title="Submit Feedback / Bug Report"):
    
    modal_title = discord.ui.TextInput(
        label="Report Title",
        placeholder="e.g. Chatbot isn't responding",
        required=True,
        max_length=100
    )
    
    modal_desc = discord.ui.TextInput(
        label="Description",
        style=discord.TextStyle.paragraph,
        description="Please provide the description",
        required=True,
        max_length=1000
    )
    
    # attachment = discord.ui.File(
    #     label="Additional Image"
    # )
    
    async def on_submit(self, interaction: discord.Interaction):
        id_channel = int(os.getenv("id_channel", 0))
        channel = interaction.client.get_channel(id_channel)
        
        if not channel:
            await interaction.response.send_message(
                "[ERROR]: Channel couldn't be found.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=f"[INFO]: New report has been retrieved with this issue: {self.modal_title.value}",
            timestamp=interaction.created_at,
        )
        
        embed.add_field(name="Submitter", value=f"{interaction.user.mention} ({interaction.user.name})", inline=True)
        embed.add_field(name="Channel Source", value=interaction.channel.mention, inline=True)
        embed.add_field(name="Description", value=self.modal_desc.value, inline=False)
        
        embed.set_footer(text=f"UserID: {interaction.user.id}")
        
        await channel.send(embed=embed)
        
        await interaction.response.send_message(
            "Thanks! We'll take care your report perfectly.",
            ephemeral=True
        )
        
    async def on_error(self, interaction: discord.Interaction, e: Exception):
        print(f"[ERROR]: Failed to submit the form {e}")
        await interaction.response.send_message(
            "There's an error while submitting your form.",
            ephemeral=True
        )
        
        