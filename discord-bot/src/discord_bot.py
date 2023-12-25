import requests
import json
import discord
import random
import re

from utils.logging_utils import MyLogger
from utils.file_reader import FileReader

# Set logging config
logger = MyLogger(__name__)


class DiscordClient(discord.Client):
    """Class used for Discord Client"""

    async def on_ready(self):
        """Print message when ready"""
        logger.info(f"Logged on as {self.user}!")

    async def on_message(self, message):
        """Activites done by bot when a message has been recieved"""
        if message.author == self.user:
            return

        if message.content.startswith("Hello"):
            logger.info(
                f"The message is: '{message.content}' from Author: '{message.author.name}'"
            )
            await message.channel.send(f"Hello {message.author.name}")

        if message.content.startswith("!quote"):
            logger.info(
                f"The message is: '{message.content}' from Author: '{message.author.name}'"
            )
            await message.channel.send(self.get_quote())

        if message.content.startswith("!challenge"):
            logger.info(
                f"The message is: '{message.content}' from Author: '{message.author.name}'"
            )
            await message.channel.send(self.get_challenge(False))

        if message.content.startswith("!list"):
            logger.info(
                f"The message is: '{message.content}' from Author: '{message.author.name}'"
            )
            await message.channel.send(self.get_challenge(True))

        if message.content.startswith("!add"):
            logger.info(
                f"The message is: '{message.content}' from Author: '{message.author.name}'"
            )
            await message.channel.send(self.add_challenge(message.content))

    def get_quote(self):
        """Returns quote from the URL"""
        logger.info("Getting a random quote.")
        response = requests.get(f"https://dummyjson.com/quotes/random", timeout=10)
        json_data = json.loads(response.text)
        output_message = json_data["quote"]
        return output_message

    def get_challenge(self, all_challenges):
        """Gets a single or list of challenges"""
        logger.info("Getting CodingChallenges.fyi challenges.")

        challenges_json = FileReader().get_file_data("challenges.json")
        json_data = (json.loads(challenges_json))["challenges"]
        output_message = ""

        if not all_challenges:
            random_number = random.randint(0, (len(json_data) - 1))
            message = json_data[random_number]
            output_message = f"{message['name']} {message['url']}"

        elif all_challenges:
            for data in json_data:
                output_message = output_message + f"{data['name']} {data['url']} \n"

        else:
            logger.error("An error occured.")
            return

        return output_message

    def add_challenge(self, challenge_message):
        """Adds the challenge to the json file"""
        logger.info("Adding URL to the list of challenges")
        message_array = challenge_message.split(" ")

        if len(message_array) > 2:
            logger.error(
                f"Message ({challenge_message}) is not valid must be `!add URL`."
            )
            return

        challenge_url = message_array[1]
        url_title = self.__validate_url(challenge_url)

        if url_title is None:
            output_message = f"Unable to add: {challenge_url} please check it is a valid Coding Challenge"
        else:
            is_present = self.__add_to_json(url_title, challenge_url)
            output_message = (
                f"Added: {url_title}: {challenge_url}"
                if is_present
                else f"Already exists: {url_title}"
            )

        return output_message

    def __validate_url(self, url):
        logger.info("Validating the URL")

        if "https://codingchallenges.fyi" not in url:
            output_message = f"Unable to add: '{url}' Invalid Domain"
            logger.error(output_message)
            return
        else:
            url_title = self.__get_html_page_title(url)

        return url_title

    def __get_html_page_title(self, message_url):
        logger.info(f"Fetching the title of the HTML page for URL: {message_url}")
        response = requests.get(message_url, timeout=10)

        if response.status_code != 200:
            logger.error(f"Invalid URL {message_url}")
            return

        title = re.search('<title data-rh="true">(.*)</title>', response.text).group(1)
        title_array = title.split("|")
        return title_array[0]

    def __add_to_json(self, title, url):
        file_path = "challenges.json"
        json_data = {"name": title, "url": url}

        data = self.__read_file(file_path)

        data_challenges = data["challenges"]
        if not any(d["name"] == title and d["url"] == url for d in data_challenges):
            logger.info(f"Adding Title: {title} and URL: {url} to file.")
            # Append the new item to the JSON array
            data["challenges"].append(json_data)

            self.__write_file(file_path, data)
            return True
        else:
            logger.error(f"Already exists: {title}")
            return False

    def __read_file(self, file_path):
        logger.info(f"Reading {file_path}")
        # Read the json file
        try:
            # Load existing JSON data from the file
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, initialize an empty list
            data = []

        return data

    def __write_file(self, file_path, data):
        logger.info(f"Writing {file_path}")
        # Write the updated data back to the file

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
