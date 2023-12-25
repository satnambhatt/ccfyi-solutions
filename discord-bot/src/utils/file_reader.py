from utils.logging_utils import MyLogger

# Set logging config
logger = MyLogger(__name__)


class FileReader:
    """Class used to get Tokens"""

    def __init__(self):
        pass

    def get_file_data(self, file):
        try:
            logger.info(f"Retrieving data from file ${file}.")
            f = open(file, "r", encoding="utf-8")
            token = f.read()
            f.close()
            return token
        except FileNotFoundError:
            logger.error(f"File ${file} does not exist")
            raise
