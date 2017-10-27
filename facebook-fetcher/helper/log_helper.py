import sys
import logging
from logging.handlers import RotatingFileHandler

def get_logger(name, maxBytes=10000000, backupCount=10):
    # logging
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]| %(message)s')
    # create a file handler
    file_handler = RotatingFileHandler('logs/' + name + '.log', maxBytes, backupCount)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    # create a stream handler 
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    # add handlers
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger