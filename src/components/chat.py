import discord
from src.service.gemini_service import get_response

async def chat_response(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    chunks = await get_response(prompt)

    await interaction.followup.send(chunks[0])
    
    for chunk in chunks[1:]:
        await interaction.channel.send(chunk)