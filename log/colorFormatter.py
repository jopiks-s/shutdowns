# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output#56944256

import logging

from colors import color


class ColorFormatter(logging.Formatter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.FORMATS = {
            logging.DEBUG: color(self._fmt, fg=(255, 255, 255)),
            logging.INFO: color(self._fmt, fg='grey'),
            logging.WARNING: color(self._fmt, fg='yellow'),
            logging.ERROR: color(self._fmt, fg='red'),
            logging.CRITICAL: color(self._fmt, fg='red', style='bold'),
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.datefmt)
        return formatter.format(record)
