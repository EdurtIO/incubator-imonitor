from flask import request

from db.model_logging_login import LoginLogging

class LoggingUtils:

    def get_logging_login(self):
        logging_login = LoginLogging()
        logging_login.ip = request.remote_addr
        return logging_login