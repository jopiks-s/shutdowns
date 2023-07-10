import logging

import config
from log.colorFormatter import ColorFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(f'{config.root_path}/log/logs/app.log', mode="w", encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s %(threadName)s %(filename)s->%(funcName)s(), line: %(lineno)d; %(message)s",
    "%m-%d %H:%M:%S"))

con_handler = logging.StreamHandler()
con_handler.setLevel(logging.DEBUG)
con_handler.setFormatter(
    ColorFormatter(fmt="%(asctime)s,%(msecs)d %(levelname)s %(module)s->%(funcName)s(); %(message)s",
                   datefmt="%H:%M:%S"))

logger.addHandler(file_handler)
logger.addHandler(con_handler)

# TODO add logging for exceptions
