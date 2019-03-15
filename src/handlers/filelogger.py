import logging as logging
import handlers.config as ConfigHandlers

#Cfg imports seem to break logging's ability to write messages
#log_cfg_list = ConfigHandlers.get_keys("FILELOGGING")

logging.basicConfig(filename="logs.txt", level=logging.DEBUG, 
					format='%(asctime)s - %(levelname)s - %(message)s', 
					filemode='a')

logger = logging.getLogger()

"""
Function to log a debug message to file
Inputs: message
Output: None
Caveats: None
"""
def log_debug_to_file(message):
	logger.debug(message)

"""
Function to log an error message to file
Inputs: message
Output: None
Caveats: None
"""
def log_error_to_file(message):
	logger.error(message)


def log_info_to_file(message):
	logger.info(message)