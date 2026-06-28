import discord
from google import genai
from src.service.gemini_service import get_response

async def handle_mention(bot: discord.Client, message: discord.Message):
    if message.author == bot.user:
        return 
    
    is_replay2bot = False
    parent_msg = None
    
    if message.reference and message.reference.message_id:
        try:
            parent_msg = await message.channel.fetch_message(message.reference.message_id)
            if parent_msg.author == bot.user:
                is_replay2bot = True
        except Exception:
            parent_msg = None
    
    if bot.user in message.mentions:
        prompt = message.content.replace(f'<@{bot.user.id}', '').strip()
        
        if not prompt and not message.attachment: 
            await message.channel.send("Hey there! Drop me a prompt after tagging me if you wanna having a conversation with me or ask me a question.")
            return 
    
        async with message.channel.typing():
            contents_payload = [] # Defining memory bucket
            
            # Memory chain
            if parent_msg:
                grandparent_msg = None
                
                if parent_msg.reference and parent_msg.reference.message_id:
                    try:
                        grandparent_msg = await message.channel.fetch_message(parent_msg.reference.message_id)
                    except:
                        grandparent_msg = None 
                        
                if grandparent_msg:
                    granpa_txt = grandparent_msg.content.replace(f'<@{bot.user.id}>', '').strip()
                    
                contents_payload.append(f"Context: You previously answered: {parent_msg.content} ")
                
            # To enable AI accessing provided files & images by user
            if message.attachments:
                for attachment in message.attachments:
                    filename = attachment.filename.lower() # Converting filename into lowercase
                    is_Img = False # Default state
                    
                    if attachment.content_type and attachment.content_type.startswith("image/"): 
                        is_Img = True
                    elif filename.endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')): # In case if attached file not started with "image/"
                        is_Img = True
                        
                    if is_Img:
                        mime = attachment.content_type or f"image/{filename.split('.')[-1]}"
                        if mime == "image/jpg":
                            mime = "image/jpeg"
                            
                        print(f"[DEBUG]: Image attachment is found with this file: '{filename}' using mime: {mime}")
                        
                        try:
                            img_bytes = await attachment.read() # Defining the variable that will convert it into bytes by reading the attachment
                            img_part = genai.types.Part.from_bytes( 
                                data = img_bytes,
                                mime_type = mime,
                            )
                            contents_payload.append(img_part) 
                            print(f"[SUCCESS]: Successfully packed image into payload. Current array size: {len(contents_payload)}")
                        except Exception as e:
                            print(f"[ERROR]: Failed converting asset: {e}")
                    else:
                        print(f"[INFO]: Ignored unrelated attachment type {filename}")
                                
                        
                        