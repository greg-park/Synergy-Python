##############################################################################
# PowerOffServers.py
# - Script for powering off servers with no profiles.
#
#   VERSION 1.0
#   Date:
#   Input: config.json
#   Output: Updates as program runs
#
#   Changes:
#
#   Notes:
#
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

print('Power off servers in profile list: [{}]'.format(get_time_stamp()))

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
    print ('Host {} not found, exiting program'.format(config['ip']))
    exit(1)

try:
    oneview_client = OneViewClient(config)
except Exception as e:
    print('Connect Error:', e)
    exit()

# Keep track of data in jsonfiles directory
json_dir = 'jsonfiles'
json_file = 'profile_list.json'

server_list = []
create_profiles = []

data_file = os.path.join(os.getcwd(),json_dir, json_file)

if os.path.isfile(data_file):
    print('{} exists for data.'.format(data_file))
    with open(data_file, 'r') as f:
        server_list = json.load(f)
else:
    print('{} not found.  File required to power off servers ... exiting'.format(data_file))
    exit()

servers_resource = oneview_client.server_hardware
# enclosure_resource = oneview_client.enclosures
# enclosures = oneview_client.enclosures.get_all()
# enclosures.sort(key=lambda x: x["name"],reverse=False)
# server_hardware_types = oneview_client.server_hardware_types

# server_hardware_type_name = config['server_hardware_type']
# enclosure_group_name = config['enclosure_group']
# profile_template_name = config['spt']
# profile_number = int(config['profile_number'])
# server_model = config['server_model']

# enc_count = 0
# for enclosure in enclosure_resource.get_all(sort='name:ascending'):
#     # pprint(enclosure)
#     enc_count = enc_count + 1
#     for db in enclosure['deviceBays']:
for server_line in server_list:
    server = servers_resource.get_by_uri(server_line['uri'])
    if server.data['powerState'] == "On":
        pprint("Server {} Power {} ... shutting down".format(server.data['name'],server.data['powerState']))
        if str(server.data['serverProfileUri']) == "None":
            if server.data['powerState'] == "On":
                server_power = server.update_power_state(configuration)
                time.sleep(10)
                print("Successfully changed the power state of server '{name}' to '{powerState}'".format(**server_power))
    else:
        pprint("Server {} Power {} already shutdown".format(server.data['name'],server.data['powerState']))
