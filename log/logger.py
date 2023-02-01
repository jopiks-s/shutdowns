import logging

from log.colorFormatter import ColorFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('app.log', mode="w")
file_handler.mode = "w"
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s %(threadName)s %(filename)s->%(funcName)s(), line: %(lineno)d, %(message)s",
    "%m-%d %H:%M:%S"))

con_handler = logging.StreamHandler()
con_handler.setLevel(logging.DEBUG)
con_handler.setFormatter(
    ColorFormatter(fmt="%(asctime)s,%(msecs)d %(levelname)s %(filename)s->%(funcName)s() %(message)s",
                   datefmt="%H:%M:%S"))

logger.addHandler(file_handler)
logger.addHandler(con_handler)

# TODO add logging for exceptions
