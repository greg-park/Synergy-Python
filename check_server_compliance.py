##############################################################################
'''
    check_server_compliance.py
    - Script for listing theservers with no profiles.

   VERSION 1.0
   Date:
   Input: config.json
   Output: json file with server info
    Create list of servers needing profiles.
    This version attempts to do more with data structures.  The goal
    is to make the code more useable AND more readable

''' 
##############################################################################

import time
import os.path
import subprocess
import platform
import json
import pprint

from config_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient
from datetime import datetime

def get_time_stamp():
    timestamp = time.time()
    date_time = datetime.fromtimestamp(timestamp)
    str_date_time = date_time.strftime('%d-%m-%Y, %H:%M:%S')
    return(str_date_time)


def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    result = subprocess.Popen(command,stdout=subprocess.PIPE)
    stdout, stderr = result.communicate()
    return (result.returncode)

print('Check server FW compliance: [{}]'.format(get_time_stamp()))

config = {
    'ip': '<oneview_ip>',
    'credentials': {
        'userName': '<username>',
        'password': '<password>',
    },
    'api_version': '<api_version>'
}
configuration = {
    'powerState': 'Off',
    'powerControl': 'PressAndHold'
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

# Ensure the OneView/Composer target exists.  If not then exit
print('Make sure OneView host {} exists ... '.
    format(config['ip']), end='')

response = ping(config['ip'])
if response == 0:
    print('Success')
else:
    print (f"Host {config['ip']} not found, exiting program")
    exit(1)

try:
    oneview_client = OneViewClient(config)
except Exception as e:
    print('Connect Error:', e)
    exit()

# Keep track of data in jsonfiles directory
JSON_DIR = 'jsonfiles'
JSON_FILE = 'compliance_list.json'

data_file = os.path.join(os.getcwd(),JSON_DIR, JSON_FILE)
if os.path.isfile(data_file):
    print(f"{data_file} exists. File will be overwritten.")
else:
    print(f"{data_file} not found ... exiting")

compliance = oneview_client.server_hardware.get_all_firmwares()
servers_resource = oneview_client.server_hardware

for x in enumerate(compliance):
    server = servers_resource.get_by_uri(x[1]['serverHardwareUri'])
    print("Checking FW for: ",server.data['name'])
    for component in x[1]['components']:
#        f_string = f"Component {component['componentName']:50s} version {component['componentVersion']}"
        print(f"Component {component['componentName']:50s} version {component['componentVersion']}")

