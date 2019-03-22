import handlers.logger as loggerhandler
import handlers.jwt as  jwthandler
from handlers.headers import SetDefaultHeaders

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
        if jwthandler.authorize_action(self, 2) == False:
            return None

        self.write(loggerhandler.get_logs())