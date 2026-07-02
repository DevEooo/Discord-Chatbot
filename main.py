import os
from dotenv import load_dotenv
from src.handler.commands import client

load_dotenv()

secret = os.getenv('discord_token')
llm = os.getenv('llm_api')

if __name__ == "__main__":
    if secret:
        client.run(secret)
    if not secret or llm:
        raise SystemExit("[ERROR]: Discord / LLM token is missing.")
    
        