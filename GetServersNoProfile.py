##############################################################################
# GetServersNoProfile.py
# - Script for listing theservers with no profiles.
#
#   VERSION 1.0
#   Date:
#   Input: config.json
#   Output: Creates a file in a local subdirectory. jsonfiles, with
#           list of servers and suggested Profile Name
############################################################################## 

from fileinput import filename
from pprint import pprint
from ConfigLoader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient
import json
#import inspect
#from itertools import ifilter

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

JSON_DIR = ".\jsonfiles\\"
# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)

print("Get list of all the servers from appliance: ")
servers = oneview_client.server_hardware.get_all()
server_profiles = oneview_client.server_profiles
profile_templates = oneview_client.server_profile_templates
enclosure_resource = oneview_client.enclosures
enclosure_groups = oneview_client.enclosure_groups
server_hardware_types = oneview_client.server_hardware_types
server_hardwares = oneview_client.server_hardware

all_templates = profile_templates.get_all()
for template in all_templates:
    if template['name'] == config["profile_template"]:
        print("Template check good")
server_hardware_type_name = config["server_hardware_type"]
enclosure_group_name = config["enclosure_group"]
profile_template_name = config["spt"]

hardware_type = server_hardware_types.get_by_name(server_hardware_type_name)
enclosure_group = enclosure_groups.get_by_name(enclosure_group_name)

for svr in servers:
    frame = svr['locationUri'].split("/")
    enclosure = enclosure_resource.get_by_uri(svr['locationUri'])
    bay = svr['position']
    if svr['state'] == "NoProfileApplied":
        bay = str(svr['position'])
        if len(bay)==1:
            i = '00'+bay
        elif len(bay)==2:
            i = '0'+bay
        elif len(bay)==3:
            i = bay
        profile_name = config['profile_name'] + i
        server_template = profile_templates.get_by_name(profile_template_name)

        print ("Enclusore: {0:s} Bay: {1:3s} Profile: {2:s} Type: {3:s} EG: {4:s}".format(enclosure.data['name'],\
            (str(bay)),profile_name,\
            server_hardware_type_name,\
            config['enclosure_group']))

        server_template = profile_templates.get_by_name(profile_template_name)
        basic_profile_options = dict(name=profile_name, serverProfileTemplateUri=server_template.data["uri"],
            serverHardwareTypeUri = hardware_type.data["uri"],
            enclosureGroupUri = enclosure_group.data["uri"]
        )
        profile = server_profiles.get_by_name(profile_name)
        if profile:
            print("Found profile with name '{}' and uri '{}'".format(profile.data['name'], profile.data['uri']))
        else:
            profile = server_profiles.create(basic_profile_options)
            print("Created profile with name '{}' and uri '{}'".format(profile.data['name'], profile.data['uri']))