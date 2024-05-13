import logging
import logging.handlers
import os

from core.config import settings


class LogManager(object):
    def __init__(self, logger_name, root_path=None):
        self.root_path = root_path

        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path)

        self.logger_name = logger_name
        self.logger = logging.getLogger(self.logger_name)

    def create_logger(self, stream=True, file=True):
        if (stream is not True) and (file is not True):
            return None
        _formatter = logging.Formatter("%(message)s")

        if stream is True:
            _stream_handler = logging.StreamHandler()
            _stream_handler.setLevel(logging.DEBUG)
            _stream_handler.setFormatter(_formatter)
            self.logger.addHandler(_stream_handler)

        if file is True:
            _file_handler = logging.handlers.WatchedFileHandler(
                filename=self.root_path + "/" + self.logger_name + ".log",
                mode="a",
                delay=False,
                encoding="utf-8",
            )
            _file_handler.suffix = "%Y%m%d"
            _file_handler.setLevel(logging.DEBUG)
            _file_handler.setFormatter(_formatter)
            self.logger.addHandler(_file_handler)

        self.logger.setLevel(logging.DEBUG)

        return self.logger


log_manager = LogManager("diane-api", settings.LOG_PATH)
api_logger = log_manager.create_logger(stream=True, file=True)
