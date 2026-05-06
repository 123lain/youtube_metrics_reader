import logging
import sys


def setup_logger():
    log_format = '%(asctime)s: %(name)-4s ||%(levelname)-4s|| %(message)s'
    date_format = '%d-%m-%Y - %H:%M'

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
