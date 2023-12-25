import logging
import sys


class MyLogger:
    """Class used for standardised logging"""

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        stream_handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(filename)s.%(funcName)s:%(lineno)d] %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        stream_handler.setFormatter(formatter)

        stream_handler.setLevel(logging.INFO)
        self.logger.addHandler(stream_handler)
        self.logger.propagate = False

    def debug(self, message):
        self.logger.debug("{}".format(message))

    def info(self, message):
        self.logger.info("{}".format(message))

    def warning(self, message):
        self.logger.warning("{}".format(message))

    def error(self, message):
        self.logger.error("{}".format(message))

    def critical(self, message):
        self.logger.critical("{}".format(message))
