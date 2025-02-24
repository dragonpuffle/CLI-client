import logging

def setup_logger():
    logger = logging.getLogger("sms_logger")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("sms_client.log")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
