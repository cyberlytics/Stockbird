import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from sys_src.backend.Constants import LOG_FILENAME, LOGFILE_PATH, LOGGER_FORMATTER


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(LOGGER_FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOGFILE_PATH / LOG_FILENAME, when="midnight", backupCount=30)
    file_handler.setFormatter(LOGGER_FORMATTER)
    file_handler.suffix = "%Y%m%d"
    return file_handler


def get_logger(logger_name: str):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger
