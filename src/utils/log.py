import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from utils import opts


LOGS_DIR = "logs/"  # will be created in output dir
LOG_FILENAME = f"{opts.PROD_NAME.lower()}.log"


def init_logger(output_dir, console_log_level):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # console
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(console_log_level)
    root_logger.addHandler(console_handler)

    # file
    log_file = Path(output_dir, LOGS_DIR, LOG_FILENAME)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=50 * 1024 * 1024,  # 50 MB
        backupCount=3,
    )
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)-5.5s] %(filename)s:%(lineno)d  %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
