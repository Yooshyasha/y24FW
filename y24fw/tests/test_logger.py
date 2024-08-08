import logging
from unittest.mock import MagicMock, patch
from loguru import logger
from y24fw.logger.logger import Logger

def test_add_file_logger():
    # Мокируем logger.add()
    with patch("loguru.logger.add") as mock_add:
        log_helper = Logger()
        log_helper.add_file_logger("data/logs/test.log")

        # Проверка: logger.add() был вызван с correct filepath
        mock_add.assert_called_once_with("data/logs/test.log", format="{level}: {time} - {message}")

def test_intercept_handler_emit():
    # Мокируем logger.log()
    with patch("loguru.logger.log") as mock_log:
        handler = Logger.InterceptHandler()
        record = logging.LogRecord("test_logger", logging.INFO, "", 0, "Test message", [], None)
        handler.emit(record)

        # Проверка: logger.log() был вызван с правильными аргументами
        mock_log.assert_called_once_with("INFO", "Test message")
