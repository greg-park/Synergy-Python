##############################################################################
# CreateProfilesFromList.py
# - Script for creating profiles based on json list of the servers with no profiles.
#
#   VERSION 1.0
#   Date:
#   Input: config.json
#   Output: simple file with list of servers without profile.
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

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)

#print("Get list of all the servers from appliance: ")
# servers = oneview_client.server_hardware.get_all()
servers = oneview_client.server_hardware
server_profiles = oneview_client.server_profiles
profile_templates = oneview_client.server_profile_templates
enclosure_resource = oneview_client.enclosures
enclosure_groups = oneview_client.enclosure_groups
server_hardware_types = oneview_client.server_hardware_types
# server_hardware = oneview_client.server_hardware

all_templates = profile_templates.get_all()
#for template in all_templates:
#    if template['name'] == config["profile_template"]:
#        print("Template check good")
server_hardware_type_name = config["server_hardware_type"]
enclosure_group_name = config["enclosure_group"]
profile_template_name = config["spt"]
profile_number = int(config["profile_number"])
server_model = config["server_model"]

hardware_type = server_hardware_types.get_by_name(server_hardware_type_name)
enclosure_group = enclosure_groups.get_by_name(enclosure_group_name)

# profile_data = []
enclosures = enclosure_resource.get_all()
f = open('profile_data.json')
profile_data = json.loads(f)
for pd in profile_data:
    print(pd)
#
#                        basic_profile_options = dict(
#                            name=profile_name,
#                            serverHardwareUri=uri,
#                            serverProfileTemplateUri=server_template.data["uri"],
#                            serverHardwareTypeUri = hardware_type.data["uri"],
#                            enclosureGroupUri = enclosure_group.data["uri"]
#                        )
#
## Double check that profile does not already exist
#                        profile = server_profiles.get_by_name(profile_name)
#                        if profile:
#                            print("Found profile with name '{}' and uri '{}'".format(profile.data['name'], profile.data['uri']))
#                        else:
## if no profile then create profile
#                            profile_data.append(basic_profile_options)
#                            # profile = server_profiles.create(basic_profile_options)
#
#### END