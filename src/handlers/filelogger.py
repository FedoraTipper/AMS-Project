import logging as logging
import handlers.config as ConfigHandlers

#Cfg imports seem to break logging's ability to write messages
#log_cfg_list = ConfigHandlers.get_keys("FILELOGGING")

logging.basicConfig(filename="logs.txt", level=logging.DEBUG, 
					format='%(asctime)s - %(levelname)s - %(message)s', 
					filemode='w')

logger = logging.getLogger()

def log_debug_to_file(message):
	logger.debug(message)

def log_error_to_file(message):
	logger.error(message)