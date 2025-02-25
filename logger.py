import logging


def setup_logger():
    logger = logging.getLogger("client")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("client.log")
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


LOGGER = setup_logger()

