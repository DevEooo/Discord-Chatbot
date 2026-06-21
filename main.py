import discord
import os
from dotenv import load_dotenv
from src.app.commands import client

load_dotenv()

secret = os.getenv('discord_token')
llm = os.getenv('llm_api')

if __name__ == "__main__":
    if secret:
        print("Logged in..")
        client.run(secret)
    else:
        print("Error")
        