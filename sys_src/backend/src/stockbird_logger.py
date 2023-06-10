import io
import sys
import sys_src.backend.src.s3_access as s3
from sys_src.backend.src.Constants import *

log_stringio = io.StringIO()


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(LOGGER_FORMATTER)
    return console_handler


def get_file_handler():
    # file_handler = RotatingFileHandler(LOGFILE_PATH / LOG_FILENAME, backupCount=30)
    file_handler = logging.StreamHandler(log_stringio)
    file_handler.setFormatter(LOGGER_FORMATTER)
    return file_handler


def get_logger(logger_name: str):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger


def write_log():
    s3.remove_log_file()
    s3.write_log(log_data=log_stringio.getvalue(), file_name=LOG_FILENAME)
