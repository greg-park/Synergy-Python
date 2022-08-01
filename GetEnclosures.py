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
from types import NoneType
from ConfigLoader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient
import json
from tabulate import tabulate

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>",
    },
    "api_version": "<api_version>"
}

JSON_DIR = ".\jsonfiles\\"
# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
try:
    oneview_client = OneViewClient(config)
except Exception as e:
    print('Connect Error:', e)
    exit()

print("Get list of all the servers MAC ids from OneView appliance: ")
servers = oneview_client.server_hardware.get_all()
# servers = oneview_client.server_hardware
server_hardwares = oneview_client.server_hardware

Profilemacs = []
NoProfilemacs = []

enclosures = oneview_client.enclosures.get_all()
enclosures.sort(key=lambda x: x["name"],reverse=False)
for enclosure in enclosures:
    for bay in enclosure["deviceBays"]:
        if bay["deviceUri"] is not None:
            if "server-hardware" in bay["deviceUri"]:
                svr = server_hardwares.get_by_uri(bay["deviceUri"])
                if svr.data['serverProfileUri'] is not None:
#                print("{} {}".format(svr.data['mpHostInfo']['mpHostName'],svr.data['mpHostInfo']['mpIpAddresses'][1]))
                    for port in svr.data["portMap"]["deviceSlots"]:
                        for pPort in port["physicalPorts"]:
                            if pPort["type"] == "Ethernet":
                                #pprint("Enclosure: {} Bay {} Port {} Mac {}".format(enclosure["name"], svr.data["position"],pPort["portNumber"],pPort["mac"]))
                                macDict = {'Enclosure': enclosure["name"], 'enclosureBay': svr.data["position"],'port': pPort["portNumber"],'macAddress': pPort["mac"]}
                                Profilemacs.append(macDict)
                else:
                    for port in svr.data["portMap"]["deviceSlots"]:
                        for pPort in port["physicalPorts"]:
                            if pPort["type"] == "Ethernet":
                                #pprint("Enclosure: {} Bay {} Port {} Mac {}".format(enclosure["name"], svr.data["position"],pPort["portNumber"],pPort["mac"]))
                                macDict = {'Enclosure': enclosure["name"], 'enclosureBay': svr.data["position"],'port': pPort["portNumber"],'macAddress': pPort["mac"]}
                                NoProfilemacs.append(macDict)

print(tabulate(Profilemacs, headers='keys', tablefmt='orgtbl'))
print("Found MACs but no profile")
print(tabulate(NoProfilemacs, headers='keys', tablefmt='orgtbl'))
