##############################################################################
# GetServersNoProfile.py
# - Script for listing theservers with no profiles.
#
#   VERSION 1.1
#   Date:
#   Input: config.json
#   Output: Creates a file in a local subdirectory. jsonfiles, with
#           list of servers and suggested Profile Name
#
#   Changes:
#       7/25/2022 - major rewrite.  
#                   - Changed to walking through enclosures
#                   - Changed naming to read data from config.json
#                       looks for profile_number and increments from there
#                   - changed some output formating
#
#   Notes:
#       Program does VERY LITTLE testing to ensure profiles are applied properly
#       Program does not verify that HW type matches the server found.
#       Program does not limit the number of profiles to apply.  Its all or nothing
#
############################################################################## 

from fileinput import filename
from pprint import pprint
from ConfigLoader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient
import json
import time, os
import platform, subprocess

def my_ping(host_or_ip, packets=1, timeout=1000):
    ''' Calls system "ping" command, returns True if ping succeeds.
    Required parameter: host_or_ip (str, address of host to ping)
    Optional parameters: packets (int, number of retries), timeout (int, ms to wait for response)
    Does not show any output, either as popup window or in command line.
    Python 3.5+, Windows and Linux compatible
    '''
    # The ping command is the same for Windows and Linux, except for the "number of packets" flag.
    print("Check OV Host: {}".format(host_or_ip))
    if platform.system().lower() == 'windows':
        command = ['ping', '-n', str(packets), '-w', str(timeout), host_or_ip]
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, creationflags=0x08000000)
        return result.returncode == 0 and b'TTL=' in result.stdout
    else:
        command = ['ping', '-c', str(packets), '-w', str(timeout), host_or_ip]
        # run parameters: discard output and error messages
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>",
    },
    "profile_name": "<profile_name>",
    "profile_template": "<profile_template>",
    "server_hardware_type": "<server_hardware_type>",
    "api_version": "<api_version>"
}
configuration = {
    "powerState": "Off",
    "powerControl": "PressAndHold"
}

JSON_DIR = ".\jsonfiles\\"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
rsp = my_ping(config['ip'])
if rsp != 0:
    oneview_client = OneViewClient(config)
else:
    print("{} OV Host Not Found ... exiting now".format(config['ip']))
    exit(1)

print("Get list of all the servers from appliance: ")
# servers = oneview_client.server_hardware.get_all()
servers = oneview_client.server_hardware
server_profiles = oneview_client.server_profiles
profile_templates = oneview_client.server_profile_templates
enclosure_resource = oneview_client.enclosures
enclosure_groups = oneview_client.enclosure_groups
server_hardware_types = oneview_client.server_hardware_types
# server_hardware = oneview_client.server_hardware

all_templates = profile_templates.get_all()
for template in all_templates:
    if template['name'] == config["profile_template"]:
        print("Template check good")
server_hardware_type_name = config["server_hardware_type"]
enclosure_group_name = config["enclosure_group"]
profile_template_name = config["spt"]
profile_number = int(config["profile_number"])
server_model = config["server_model"]

hardware_type = server_hardware_types.get_by_name(server_hardware_type_name)
enclosure_group = enclosure_groups.get_by_name(enclosure_group_name)

enc_count = 0
dbcnt = 0
created_profiles = []

for enclosure in enclosure_resource.get_all(sort='name:ascending'):
    enc_count = enc_count + 1
    dbcnt = 0
    for db in enclosure['deviceBays']:
        dbcnt = dbcnt+1
        if "server-hardware" in (str(db['deviceUri'])):
            svr = servers.get_by_uri(db['deviceUri'])
            if (svr.data['serverHardwareTypeUri']) == (hardware_type.data["uri"]):
                if str(svr.data['serverProfileUri']) == "None":
                    pprint("Enclosure {} Device Bay {} Device {} Power {}".format(enc_count, dbcnt, db['devicePresence'],svr.data['powerState']))
                    if svr.data['powerState'] == "On":
                        print("'{}' skipped due to power state '{}'".format(svr.data['name'],svr.data['powerState']))
                    else:
                        bay = str(profile_number)
                        profile_name = config['profile_name']+str(profile_number)
                        print("Set server profile for '{}' as {}".format(svr.data['name'],profile_name))
                       
                        profile_number = profile_number+1
                        try:
                            server_template = profile_templates.get_by_name(profile_template_name)
                            profile = server_template.get_new_profile()
                        except:
                            print("Failed to create profile {} from template {}... exiting".format(profile_name, profile_template_name))
                            exit(1)
                       
                        uri = str(svr.data['uri'])
                        profile['name'] = profile_name
                        profile['serverHardwareUri'] = uri

                        try:
                            print("Applying profile {}".format(profile_name))
                            created_profiles.append(server_profiles.create(profile, timeout=5))
                        except:
                            pass

print("Some error checking")
print (created_profiles)