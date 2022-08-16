##############################################################################
'''
    apply_server_profiles.py
    - Script to apply profiles to servers with no profiles.
          reads info from file and applies profiles to files listed

      VERSION 1.0
      Date:
      Input: config.json, servers.json
          Note that servers.json is really just a dictionary

      Output: Creates a file in a local subdirectory. jsonfiles, with
              list of servers and suggested Profile Name

      Changes:
          8/1/2022 - rewrite to adopt PEP-8 formating
                  - name change to lower case and underscore
                  - updated functions to PEP-8 format

      Notes:
          Program does VERY LITTLE testing to ensure profiles are applied properly
          Program does not verify that HW type matches the server found.
          Program does not limit the number of profiles to apply.  Its all or nothing

'''

import time
import os.path
import subprocess
import platform
import pprint
import json

from zmq import device

from config_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient
from datetime import datetime

def get_time_stamp():
    '''
    function used to timestamp program
    '''
    timestamp = time.time()
    date_time = datetime.fromtimestamp(timestamp)
    str_date_time = date_time.strftime('%d-%m-%Y, %H:%M:%S')
    return str_date_time

def ping(host):
    '''
    Function to check server availablility
    '''
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    result = subprocess.Popen(command,stdout=subprocess.PIPE)
    stdout, stderr = result.communicate()
    return result.returncode

def apply_server_profiles(profiles):
    '''
    function apply_server_profiles
    '''
    for profile_to_create in profiles:
        server = oneview_client.server_hardware.get_by_uri(profile_to_create['uri'])
        print("Server: ", server.data['name'])

        try:
            server_template = oneview_client.server_profile_templates.get_by_name(config['profile_template'])
            profile = server_template.get_new_profile()
        except:
            print("Failed to create profile {} from template {}... exiting".format(profile_to_create['profileName'], profile_to_create['template']))
            exit(1)
#                
        profile['name'] = profile_to_create['profileName']
        profile['serverHardwareUri'] = profile_to_create['uri']
        try:
            print("Applying profile {} to {}".format(server.data['name'],profile_name))
            oneview_client.server_profiles.create(profile, timeout=5)
        except:
            pass

#####

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
    exit(1)

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
    print('{} not found.  File required to create profiles ... exiting'.format(data_file))
    exit()

servers_resource = oneview_client.server_hardware
enclosure_resource = oneview_client.enclosures
profile_template_resource = oneview_client.server_profile_templates
server_hardware_types_resource = oneview_client.server_hardware_types
server_profiles_resource = oneview_client.server_profiles

profile_number = int(config['profile_number'])
profile_name = config['profile_name']

templates = profile_template_resource.get_all()
hardware_type = server_hardware_types_resource.get_by_name(config['server_hardware_type'])

if hardware_type:
    print("{} Hardware type check good".format(config['server_hardware_type']))

template_check = False
for template in templates:
    if template['name'] == config['profile_template']:
        template_check = True

if template_check:
    print("{} Server Profile Template exists".format(config['profile_template']))
else:
    print("{} Server Profile Template not found".format(config['profile_template']))

for server_line in server_list:
    server = servers_resource.get_by_uri(server_line['uri'])
    if (server.data['serverHardwareTypeUri']) == (hardware_type.data["uri"]):
        if server.data['state'] == 'NoProfileApplied':
            if server.data['powerState'] == "On":
                print("'{}' skipped due to power state '{}'".format(server.data['name'],server.data['powerState']))
            else:
#                enc = enclosure_resource.get_by_uri(server.data['locationUri'])
                profile_name = config['profile_name']+str(profile_number)
                profile_number = profile_number+1
                tDict = {'uri':server.data['uri'], 'template': config['profile_template'], 'profileName':profile_name}
                create_profiles.append(tDict)

apply_server_profiles(create_profiles)