##############################################################################
# CreateListServersNoProfile.py
# - Script for creating a list of the servers with no profiles.
#
#   VERSION 1.0
#   Date:
#   Input: config.json
#   Output: simple file with list of servers without profile.
#               server location URI
#
#   Changes:
#
#   Notes:
#
############################################################################## 

from fileinput import filename
from ConfigLoader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient
import sys
import json

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

profile_data = []
enclosures = enclosure_resource.get_all()
# Loop through all the enclosures enumerated 
for count, item in enumerate(enclosures):
    print("Checking Enclosure {} device bays".format(count))
    enclosure = enclosures[count]
    for db in enclosure['deviceBays']:
# loop through each of the device bays (db)
        if "server-hardware" in (str(db['deviceUri'])):
            svr = servers.get_by_uri(db['deviceUri'])
# check the dict variable data[serverHardwareTypeURI] vs uri of HW type
            if (svr.data['serverHardwareTypeUri']) == (hardware_type.data["uri"]):
# we found the matching HW
# Now check the profile URI.  If it is set to None then no profile exists
                if str(svr.data['serverProfileUri']) == "None":
                    print("Enclosure:{:2s} Device Bay:{:2s} Server Model:{:20s} Power:{:3s}".format(str(count), str(db['bayNumber']), svr.data['model'],svr.data['powerState']))
# Check the power and if ON then skip this server
                    if svr.data['powerState'] == "On":
                        print("Skipping server '{}' power is '{}'".format(svr.data['name'],svr.data['powerState']))
                    else:
# Power is off so build the profile name by padding the bay number
#                        bay = str(profile_number)
                        bay = str(db['bayNumber'])
                        if str(db['profileUri']) == "None":
                            if len(bay)==1:
                                i = '00'+bay
                            elif len(bay)==2:
                                i = '0'+bay
                            elif len(bay)==3:
                                i = bay

# Build the profile name based off profile_name in config.json+enclosure#+bay
# Note: Enclosure number is based off the sorted list.  List is sorted on enclosure INTERNAL name
                        profile_name = config['profile_name'] + "_"+str(count)+"_"+str(i)
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

# Double check that profile does not already exist
                        profile = server_profiles.get_by_name(profile_name)
                        if profile:
                            print("Found profile with name '{}' and uri '{}'".format(profile.data['name'], profile.data['uri']))
                        else:
# if no profile then create profile
                            profile_data.append(basic_profile_options)
                            # profile = server_profiles.create(basic_profile_options)

if profile_data:
    with open('profile_data.json', 'w') as f:
        for pd in profile_data:
            json.dump(pd,f)

### END