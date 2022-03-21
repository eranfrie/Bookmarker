import logging


def init_logger():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # console
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
