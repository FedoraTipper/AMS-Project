import configparser

file = "config/config"

def get_keys(section):
	config = configparser.ConfigParser()
	config.read(file)
	config_list = list()
	for key in config[section]:
		config_list.append(config[section][key])
	return config_list