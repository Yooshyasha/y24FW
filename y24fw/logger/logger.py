import logging
from loguru import logger

logger.add("data/logs/log_{time}.log", format="{level}: {time} - {message}")


class InterceptHandler(logging.Handler):
    def emit(self, record):
        level = logger.level(record.levelname).name
        logger.log(level, record.getMessage())


logging.getLogger('aiogram').setLevel(logging.DEBUG)
logging.getLogger('aiogram').addHandler(InterceptHandler())
