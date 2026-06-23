import discord
from src.service.gemini_service import get_response

async def handle_mention(bot: discord.Client, message: discord.Message):
    if message.author == bot.user:
        return 
    
    if bot.user in message.mentions:
        prompt = message.content.replace(f'<@{bot.user.id}', '').strip()
        
        if not prompt: 
            await message.channel.send("Hey there! Drop me a prompt after tagging me if you wanna having a conversation with me or ask me a question.")
            return 
    
        async with message.channel.typing():
            chunks = await get_response(prompt)
            for chunk in chunks:
                await message.channel.send(chunk)