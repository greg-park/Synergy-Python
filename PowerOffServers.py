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
}
configuration = {
    "powerState": "Off",
    "powerControl": "PressAndHold"
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)

print("Get list of all the servers from appliance: ")
servers = oneview_client.server_hardware
enclosure_resource = oneview_client.enclosures
server_hardware_types = oneview_client.server_hardware_types
server_hardware_type_name = config["server_hardware_type"]
hardware_type = server_hardware_types.get_by_name(server_hardware_type_name)

enc_count = 0
for enclosure in enclosure_resource.get_all(sort='name:ascending'):
    # pprint(enclosure)
    enc_count = enc_count + 1
    for db in enclosure['deviceBays']:
        if "server-hardware" in (str(db['deviceUri'])):
            svr = servers.get_by_uri(db['deviceUri'])
            if (svr.data['serverHardwareTypeUri']) == (hardware_type.data["uri"]):
                pprint("Enclosure {} Device {} Power {}".format(enc_count, db['devicePresence'],svr.data['powerState']))
                if str(svr.data['serverProfileUri']) == "None":
                    if svr.data['powerState'] == "On":
                        server_power = svr.update_power_state(configuration)
#                       Sleep for 10 seconds to allow for power to shutdown.  Servers take at least
#                       6 seconds.  This prevents problems with applying profiles too quickly
                        time.sleep(10)
                        print("Successfully changed the power state of server '{name}' to '{powerState}'".format(**server_power))
