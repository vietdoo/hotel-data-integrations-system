import logging
import os
import sys
from datetime import datetime
from configs.config import logger_config

class Logger:
    def __init__(self, log_dir, log_level):
        self.log_dir = log_dir
        self.log_level = log_level
        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_level)
        self.formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)
        self.file_handler = None
        self.create_log_file()

    def create_log_file(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        log_file = os.path.join(
            self.log_dir, datetime.now().strftime('%Y-%m-%d_%H-%M-%S.log'))
        self.file_handler = logging.FileHandler(log_file)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def log(self, message, level='info'):
        if level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'critical':
            self.logger.critical(message)
        else:
            self.logger.debug(message)

    def enable_console_log(self):
        """Enable console logging."""
        if not any(isinstance(h, logging.StreamHandler) for h in self.logger.handlers):
            self.logger.addHandler(self.console_handler)

    def disable_console_log(self):
        """Disable console logging."""
        if self.console_handler in self.logger.handlers:
            self.logger.removeHandler(self.console_handler)

    def close(self):
        self.disable_console_log()
        if self.file_handler:
            self.logger.removeHandler(self.file_handler)
            self.file_handler.close()

logger = Logger(logger_config['log_dir'], logger_config['log_level'])

if not logger_config['enable_console_logging']:
    logger.disable_console_log()
