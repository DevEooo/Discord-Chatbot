import discord
from google import genai
from src.service.gemini_service import get_response
from src.utils.chunks import split_into_chunks

async def handle_mention(bot: discord.Client, message: discord.Message):
    if message.author == bot.user:
        return 
    
    is_reply2bot = False
    parent_msg = None
    
    if message.reference and message.reference.message_id:
        try:
            parent_msg = await message.channel.fetch_message(message.reference.message_id)
            if parent_msg.author == bot.user:
                is_reply2bot = True
        except Exception:
            parent_msg = None
    
    if bot.user in message.mentions or is_reply2bot:
        prompt = message.content.replace(f'<@{bot.user.id}', '').strip()
        
        if not prompt and not message.attachments: 
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
                
            # To enable AI accessing provided images by user
            if message.attachments:
                for attachment in message.attachments:
                    filename = attachment.filename.lower() # Converting filename into lowercase
                    mime = attachment.content_type
                   
                    if not mime:
                        if filename.endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                            mime = f"image/{filename.split('.'[-1])}"
                        elif filename.endswith('.pdf'):
                            mime = "application/pdf"
                        elif filename.endswith(('.txt', '.md', 'html')):
                            mime = "text/plain"
                            
                    if mime == "image/jpg":
                        mime = "image/jpeg"
                        
                    is_supported = False
                    if mime and (mime.startswith("image/") or mime == "application/pdf" or mime == "text/plain"):
                        is_supported = True
                    
                    if is_supported:
                        print(f"[DEBUG]: Processing supported asset '{filename}' using mime: {mime}")
                        
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
                                
        if prompt:
            contents_payload.append(prompt)
        elif not prompt and len(contents_payload) > 0:
            contents_payload.append("Analyzing provided attachments directly...")
        
        print(f"[INFO]: Sending payloads containing {len(contents_payload)} components directly to LLM...")
        
        chunks = await get_response(contents_payload)
        
        if chunks:
            await message.reply(chunks[0])
            for chunk in chunks[1:]:
                await message.channel.send(chunk)
                