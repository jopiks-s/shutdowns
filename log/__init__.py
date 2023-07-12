import os
from config import root_path

logs_dir = f'{root_path}/log/logs'
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

from ._logger import logger
from ._request_logger import request_logger
