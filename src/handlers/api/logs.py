import utilities.error as ErrorUtil
import handlers.logger as LoggerHandler
import handlers.jwt as  JWTHandler
from handlers.headers import SetDefaultHeaders

import utilities.error as ErrorUtil

class Log(SetDefaultHeaders):
    """
    Class to handle log API requests
    Functions: get, post, put, delete
    """
    def get(self):
        """
        Function to get logs or a single log record
        Inputs: Tornado web request
        Output: Log data
        Caveats: Authentication needs to be passed
        """
        if JWTHandler.authorize_action(self, 2) == False:
            return None

        self.write(LoggerHandler.get_logs())