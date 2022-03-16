# Python Script to read all info 
###
# ADapted from config_loader.py in HPE iLO and HPE OneView
# Python github repo
# 
# Adaptations
#   Name: ReadInfo.py
###

from future import standard_library
standard_library.install_aliases()

import json
import os

CUR_MODULE_DIR = os.path.dirname(__file__)
DEFAULT_CONFIG_FILE = os.path.join(CUR_MODULE_DIR, 'config.json')

def try_load_from_file(config, file_name=None):
    if not file_name:
        file_name = DEFAULT_CONFIG_FILE

    if not os.path.isfile(file_name):
        return config

    with open(file_name) as json_data:
        return json.load(json_data)


# main

# initially data is based on a range assumption.  Given a number of
# enclosures and servers the names will be built as
# enclosure_name## with ## the range of 01 to num_enclosures
# AND
# host_name## with ## the range of 01 to num_hosts
# both lists are inclusive of 01 and ##
appliance_info = try_load_from_file(config)
print(json_data.enclosure_ip_range)
#print(enclosure_name_list)
#print(enclosure_host_list)
#print(number_of_enclosures)
#print(num_hosts)