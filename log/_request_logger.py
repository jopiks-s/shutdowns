import logging

import config

request_logger = logging.getLogger(__name__)
request_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(f'{config.root_path}/log/logs/requests.log', mode="w")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s.%(msecs)03d %(levelname)s %(threadName)s %(funcName)s(), line: %(lineno)d;\n%(message)s",
    "%m-%d %H:%M:%S"))

request_logger.addHandler(file_handler)
