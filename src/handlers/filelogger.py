import logging as logging
import handlers.config as ConfigHandlers

#Cfg imports seem to break logging's ability to write messages
#log_cfg_list = ConfigHandlers.get_keys("FILELOGGING")

logging.basicConfig(filename="app.log", level=logging.DEBUG, 
					format='%(asctime)s - %(levelname)s - %(message)s', 
					filemode='a')

logger = logging.getLogger()

def log_debug_to_file(message):
	"""
	Function to log a debug message to file
	Inputs: message
	Output: None
	Caveats: None
	"""
	logger.debug(message)

def log_error_to_file(message):
	"""
	Function to log an error message to file
	Inputs: message
	Output: None
	Caveats: None
	"""
	logger.error(message)


def log_info_to_file(message):
	"""
	Function to log an info message to file
	Inputs: message
	Output: None
	Caveats: None
	"""
	logger.info(message)