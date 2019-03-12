import configparser

file = "config/config"

"""
Function to handle the retrieving of config data from the config file
Inputs: Section of config that will be returned
Output: List of config data
Caveats: None
"""
def get_keys(section):
	config = configparser.ConfigParser()
	config.read(file)
	config_list = list()
	for key in config[section]:
		config_list.append(config[section][key])
	return config_list