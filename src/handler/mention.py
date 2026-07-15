import time
import discord
from discord.utils import escape_mentions
from google import genai
from src.service.gemini_service import get_response

USER_COOLDOWN_SECONDS = 10.0
CHANNEL_COOLDOWN_SECONDS = 5.0
MAX_ATTACHMENT_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_ATTACHMENT_PREFIXES = ("image/", "application/pdf")
ALLOWED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".gif")

user_cooldowns: dict[int, float] = {}
channel_cooldowns: dict[int, float] = {}

async def handle_mention(bot: discord.Client, message: discord.Message):
    if message.author == bot.user:
        return

    now = time.monotonic()
    last_user = user_cooldowns.get(message.author.id, 0)
    last_channel = channel_cooldowns.get(message.channel.id, 0)

    if now - last_user < USER_COOLDOWN_SECONDS:
        remaining = USER_COOLDOWN_SECONDS - (now - last_user)
        await message.reply(
            f"Please wait {remaining:.0f}s before asking me again.",
            mention_author=False,
        )
        return

    if now - last_channel < CHANNEL_COOLDOWN_SECONDS:
        remaining = CHANNEL_COOLDOWN_SECONDS - (now - last_channel)
        await message.reply(
            f"This channel is busy. Try again in {remaining:.0f}s.",
            mention_author=False,
        )
        return

    user_cooldowns[message.author.id] = now
    channel_cooldowns[message.channel.id] = now

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
        prompt = message.content.replace(f"<@{bot.user.id}>", "").strip()
        prompt = escape_mentions(prompt)

        if not prompt and not message.attachments:
            await message.channel.send(
                "Please include a question or prompt when you mention me."
            )
            return

        async with message.channel.typing():
            contents_payload = []
            supported_attachment_found = False

            if parent_msg:
                parent_text = escape_mentions(parent_msg.content)
                contents_payload.append(
                    f"Conversation context: The user previously asked '{parent_text}'."
                )

                if parent_msg.reference and parent_msg.reference.message_id:
                    try:
                        grandparent_msg = await message.channel.fetch_message(
                            parent_msg.reference.message_id
                        )
                        grandparent_text = escape_mentions(grandparent_msg.content)
                        contents_payload.append(
                            f"Earlier context: '{grandparent_text}'."
                        )
                    except Exception:
                        pass

            for attachment in message.attachments:
                filename = attachment.filename.lower()
                mime = attachment.content_type

                if not mime:
                    if filename.endswith(ALLOWED_IMAGE_EXTENSIONS):
                        mime = f"image/{filename.rsplit('.', 1)[-1]}"
                    elif filename.endswith(".pdf"):
                        mime = "application/pdf"

                if mime == "image/jpg":
                    mime = "image/jpeg"

                if (
                    not mime
                    or not mime.startswith(ALLOWED_ATTACHMENT_PREFIXES)
                    or attachment.size > MAX_ATTACHMENT_SIZE
                ):
                    continue

                supported_attachment_found = True
                try:
                    file_bytes = await attachment.read()
                    part = genai.types.Part.from_bytes(data=file_bytes, mime_type=mime)
                    contents_payload.append(f"Attachment: {filename}")
                    contents_payload.append(part)
                except Exception as e:
                    print(f"[ERROR]: Failed converting asset {filename}: {e}")
                    await message.channel.send(
                        "I could not process one of the attachments. Please retry without it."
                    )
                    return

            if not prompt and not supported_attachment_found:
                await message.channel.send(
                    "I can only process image and PDF attachments when no prompt is provided."
                )
                return

            if prompt:
                contents_payload.append(prompt)
            elif supported_attachment_found:
                contents_payload.append(
                    "Please analyze the attached content and answer the user's request."
                )

            chunks = await get_response(contents_payload)

            if chunks:
                await message.reply(chunks[0], mention_author=False)
                for chunk in chunks[1:]:
                    await message.channel.send(chunk)
                