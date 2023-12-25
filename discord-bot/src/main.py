import discord

from utils.logging_utils import MyLogger
from utils.file_reader import FileReader
from discord_bot import DiscordClient

# Set logging config
logger = MyLogger(__name__)


def main():
    """Main Function"""
    logger.info("Getting token for Discord bot")
    discord_token = FileReader().get_file_data(".secrets/api_key")

    logger.info("Starting discord bot...")
    intents = discord.Intents.default()
    intents.message_content = True
    client = DiscordClient(intents=intents)
    client.run(discord_token, log_handler=None)  # Replace with your own token


if __name__ == "__main__":
    main()
