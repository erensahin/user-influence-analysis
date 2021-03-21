"""
BLG517E - Spring 2019 Term Project
User Influence Analysis for GitHub Developer Social Networks
Sefa Eren Sahin
504171526
"""

import logging
import sys


def setup_custom_logger(name="default_logger", log_file=None):
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    file_handler = None
    if log_file is not None:
        file_handler = logging.FileHandler('log.txt', mode='w')
        file_handler.setFormatter(formatter)

    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(screen_handler)

    if file_handler is not None:
        logger.addHandler(file_handler)

    return logger
