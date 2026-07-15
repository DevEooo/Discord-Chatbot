import logging
import os
from dotenv import load_dotenv
from src.handler.commands import client

load_dotenv()

secret = os.getenv("discord_token")
llm = os.getenv("llm_credential")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    if not secret or not llm:
        raise SystemExit(
            "[ERROR]: Missing required credentials. "
            "Ensure both discord_token and llm_credential are set in your environment."
        )

    logger.info("Starting bot with validated credentials.")
    client.run(secret)
    
        