import logging

from loguru import logger

class Logger:
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            level = logger.level(record.levelname).name
            logger.log(level, record.getMessage())

    def __init__(self):
        self.logger = logger

    def add_logger(self, name: str, level: int):
        logging.getLogger(name).setLevel(level)
        logging.getLogger(name).addHandler(self.InterceptHandler())

    def add_file_logger(self, filepath: str = "data/logs/log_{time}.log"):
        logger.add(filepath, format="{level}: {time} - {message}")
