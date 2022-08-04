##############################################################################
# find_severs_noprofile.py
# - Script for listing theservers with no profiles.
#
#   VERSION 1.1
#   Date:
#   Input: config.json
#   Output: Creates a file in a local subdirectory. jsonfiles, with
#           list of servers and suggested Profile Name
#
#   Changes:
#       8/1/2022 - rewrite to adopt PEP-8 formating
#               - name change to lower case and underscore
#               - updated functions to PEP-8 format
#
#   Notes:
#       Program does VERY LITTLE testing to ensure profiles are applied properly
#       Program does not verify that HW type matches the server found.
#       Program does not limit the number of profiles to apply.  Its all or nothing
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

print('Apply profiles to all servers: [{}]'.format(get_time_stamp()))

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
if ping (config['ip']) == 0:
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

data_file = os.path.join(os.getcwd(),json_dir, json_file)
if os.path.isfile(data_file):
    print('{} exists. File will be overwritten, with warning but without remorse'.format(data_file))
else:
    print('{} not found.  File required to create profiles ... exiting'.format(data_file))
    exit()

servers = oneview_client.server_hardware
enclosure_resource = oneview_client.enclosures
# server_hardware_types = oneview_client.server_hardware_types

server_hardware_type_name = config['server_hardware_type']
enclosure_group_name = config['enclosure_group']
profile_template_name = config['spt']
profile_number = int(config['profile_number'])
server_model = config['server_model']

create_profiles = []

for enclosure in enclosure_resource.get_all():
# Check each device bay for a reference uri
    for bay in enclosure['deviceBays']:
        if bay['deviceUri'] is not None:
            if 'server-hardware' in bay['deviceUri']:
                server = servers.get_by_uri(bay['deviceUri'])
                sht = oneview_client.server_hardware_types.get_by_uri(server.data['serverHardwareTypeUri'])
                if sht.data['name'] == config['server_hardware_type']:
                    print(sht.data['name'])
                    if server.data['state'] == 'NoProfileApplied':
                        profile_name = config['profile_name']+str(profile_number)
                        profile_number = profile_number+1
                        uri = server.data['locationUri']
                        enc = enclosure_resource.get_by_uri(uri)
                        tDict = {'uri':server.data['uri'], 'template': profile_template_name, 'profileName': profile_name}
                        create_profiles.append(tDict)
                else:
                    print("Hardware {} does not match HW template {}".format(sht.data['name'], config['server_hardware_type']))

with open(data_file, 'r+') as server_list:
    json.dump(create_profiles, server_list)

total_profiles = profile_number - int(config['profile_number'])
print("Total Servers needing profiles: ",total_profiles)
for prof in create_profiles:
    print(prof)