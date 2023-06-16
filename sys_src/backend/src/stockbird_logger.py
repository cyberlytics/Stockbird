import io
import sys
import sys_src.backend.src.s3_access as s3
from sys_src.backend.src.Constants import *

log_stringio = io.StringIO()


def get_console_handler():
    """Handles logging on Console"""
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(LOGGER_FORMATTER)
    return console_handler


def get_file_handler():
    """Handles logging into the S3 Bucket"""
    file_handler = logging.StreamHandler(log_stringio)
    file_handler.setFormatter(LOGGER_FORMATTER)
    return file_handler


def get_logger(logger_name: str):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger


def write_log():
    """This function triggers the creation of a log file on the S3 Bucket
    Because of the S3 bucket we need to do the handling for file creation by our own,
    if more than 30 log files are on the S3 Bucket the oldest one gets deleted.
    if a log file for today already exists we will append the logging information to this file"""

    s3.try_remove_oldest_log()
    if s3.exists_log_for_today():
        s3.update_log(log_stringio.getvalue(), LOG_FILENAME)
    else:
        s3.write_log(log_stringio.getvalue(), LOG_FILENAME)
