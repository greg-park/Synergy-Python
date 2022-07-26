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
import time

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
oneview_client = OneViewClient(config)

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
count = 0
dbcnt = 0
profile_list = []

for enclosure in enclosure_resource.get_all(sort='name:ascending'):
    # pprint(enclosure)
    enc_count = enc_count + 1
    dbcnt = 0
    for db in enclosure['deviceBays']:
        dbcnt = dbcnt+1
        if "server-hardware" in (str(db['deviceUri'])):
            count = count+1
            svr = servers.get_by_uri(db['deviceUri'])

            if (svr.data['serverHardwareTypeUri']) == (hardware_type.data["uri"]):
                if str(svr.data['serverProfileUri']) == "None":
                    pprint("Enclosure {} Device Bay {} Device {} Power {}".format(enc_count, dbcnt, db['devicePresence'],svr.data['powerState']))
                    if svr.data['powerState'] == "On":
                        server_power = svr.update_power_state(configuration)
#                       Sleep for 10 seconds to allow for power to shutdown.  Servers take at least
#                       6 seconds.  This prevents problems with applying profiles too quickly
                        time.sleep(10)
                        print("Successfully changed the power state of server '{name}' to '{powerState}'".format(**server_power))

                    bay = str(profile_number)
                    if str(db['profileUri']) == "None":
                        if len(bay)==1:
                            i = '00'+bay
                        elif len(bay)==2:
                            i = '0'+bay
                        elif len(bay)==3:
                            i = bay
 
                    profile_name = config['profile_name'] + "_"+str(enc_count)+"_"+str(i)
                    profile_number = profile_number+1
                    server_template = profile_templates.get_by_name(profile_template_name)
                    uri = str(svr.data['uri'])
                    basic_profile_options = dict(
                        name=profile_name,
                        serverHardwareUri=uri,
                        serverProfileTemplateUri=server_template.data["uri"],
                        serverHardwareTypeUri = hardware_type.data["uri"],
                        enclosureGroupUri = enclosure_group.data["uri"]
                    )
                    
                    profile = server_profiles.get_by_name(profile_name)
                    if profile:
                        print("Found profile with name '{}' and uri '{}'".format(profile.data['name'], profile.data['uri']))
                    else:
                        profile = server_profiles.create(basic_profile_options)
                        print("Create profile with name '{}'".format(profile_name))
                        # server_profiles.create()
                        profile_list.append(profile)
