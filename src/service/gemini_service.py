import logging
import os
from dotenv import load_dotenv
from google import genai
from src.utils.chunks import split_into_chunks
from pathlib import Path

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

base_dir = Path(__file__).resolve().parent
prompt_path = base_dir.parent.parent / "prompt.txt"

if not prompt_path.exists():
    raise SystemExit("[ERROR]: prompt.txt is missing. Create prompt.txt before starting the bot.")

with open(prompt_path, "r", encoding="utf-8") as file:
    prompt_instruction = file.read().strip()

if not prompt_instruction:
    raise SystemExit("[ERROR]: prompt.txt is empty. Add a fixed system prompt before starting the bot.")

llm_api_key = os.getenv("llm_credential")
if not llm_api_key:
    raise SystemExit("[ERROR]: LLM credential is missing. Set llm_credential in environment.")

ai_client = genai.Client(api_key=llm_api_key)

async def get_response(contents: list) -> list[str]:
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=genai.types.GenerateContentConfig(
                system_instruction = prompt_instruction
            )
        )
        
        return split_into_chunks(response.text)

    except Exception as e:
        logger.error("LLM request failed: %s", e)
        return ["Apologies, I could not process your request at the moment."]