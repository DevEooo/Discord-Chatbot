import os
from dotenv import load_dotenv
from src.handler.commands import client

load_dotenv()

secret = os.getenv('discord_token')
llm = os.getenv('llm_api')

if __name__ == "__main__":
    if not llm:
        raise SystemExit("[ERROR]: LLM token is missing.")
    if not secret:
        raise SystemExit("[ERROR]: Discord token is missing.")
    if not secret and llm:
        raise SystemExit("[ERROR]: Both Discord and LLM token are missing.")
    
    client.run(secret)
    
        