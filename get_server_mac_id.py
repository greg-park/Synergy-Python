##############################################################################
# get_server_mac_id.py
# - Script for listing the servers physical NIC MAC IDs.
#
#   VERSION 1.0
#   Date:
#   Input: config.json
#   Output: Creates a list to STDOUT of the MAC ids found.
#           That list is printed as 
#           EnclosureName Bay ServerPort Mac
#########0#########1#########2#########3#########4#########5#########6#########7#########

import time
import os.path
import subprocess
import platform

from config_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient
from datetime import datetime

def get_time_stamp():
    timestamp = time.time()
    date_time = datetime.fromtimestamp(timestamp)
    str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
    return(str_date_time)

def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    result = subprocess.Popen(command,stdout=subprocess.PIPE)
    stdout, stderr = result.communicate()
    return (result.returncode)

print("List all server MAC ids from OneView appliance: [{}]".
    format(get_time_stamp()))

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>",
    },
    "api_version": "<api_version>"
}

# Keep track of data in jsonfiles directory
JSON_DIR = "./jsonfiles"
# Make sure that directory exists
print("Make sure {} exists for data.  Path check = {}".
    format(JSON_DIR, os.path.isdir(JSON_DIR)))

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

# Ensure the OneView/Composer target exists.  If not then exit
print("Make sure OneView host {} exists ... ".
    format(config["ip"]), end="")
if ping (config["ip"]) == 0:
    print("Success")
else:
    print ("Host {} not found, exiting program".format(config["ip"]))
    exit(1)

try:
    oneview_client = OneViewClient(config)
except Exception as e:
    print('Connect Error:', e)
    exit()

servers = oneview_client.server_hardware.get_all()
server_hardwares = oneview_client.server_hardware

# Create empty dictionaries for storing the MAC info.
# Grab all the Enclosures and sort that list by enclosure name
enclosures = oneview_client.enclosures.get_all()
enclosures.sort(key=lambda x: x["name"],reverse=False)

# Walk through all the enclosures ...
# Note, this is not necessary but done here
# to allow for sorting the Enclosures.
# Another option would be to simply grab all the 
# server profiles and print out the conneciton info.

for enclosure in enclosures:
# Check each device bay for a reference uri
    for bay in enclosure["deviceBays"]:
        if bay["deviceUri"] is not None:
# Make sure this is a ServerHardware URI
            if "server-hardware" in bay["deviceUri"]:
                svr = server_hardwares.get_by_uri(bay["deviceUri"])

# Check that the server has a profile applied then ...
# walk through the ports (connections) and print out the MACs
                if svr.data['serverProfileUri'] is not None:
                    server_profile = oneview_client.server_profiles.get_by_uri \
                                        (svr.data['serverProfileUri'])

                    for connection in server_profile.data["connectionSettings"]["connections"]:
                        if connection["functionType"] == "Ethernet":
                            print("{} {} {} {}".format(enclosure["name"],
                                                    svr.data["position"],
                                                    connection["id"], 
                                                    connection["mac"]))


print("\nFinished: {}".format(get_time_stamp()))