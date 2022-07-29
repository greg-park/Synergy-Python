##############################################################################
# GetMACID.py
# - Script for listing the MAC IDs for servers with applied profiles.
#
#   VERSION 1.0
#   Date:
#   Input: config.json
#   Output: Creates a file in a local subdirectory. jsonfiles, with
#           list of Frame, Bay, MAC ID, Card
############################################################################## 
###

from pprint import pprint
from fileinput import filename
from ConfigLoader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>",
    },
    "api_version": "<api_version>"
}
 
# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
JSON_DIR = ".\jsonfiles\\"
 
print("Get list of all the server MAC IDs from appliance: ")
servers = oneview_client.server_hardware.get_all()
enclosure_resource = oneview_client.enclosures

outfile=JSON_DIR+"serverMAC.json"
of = open(outfile,"w")
for svr in servers:
#    if svr['state'] == "ProfileApplied":
        frame = svr['locationUri'].split("/")
        enclosure = enclosure_resource.get_by_uri(svr['locationUri'])
        location = frame[len(frame)-1]
        bay = svr['position']
        print ("Enclusore: {0:s} Bay: {1:s} ProfileSate: {2:s}".format(enclosure.data['name'],(str(bay)),svr['state']))
        for slot in svr['portMap']['deviceSlots']:
            macID = location + ',' + str(bay)
            of.write(macID)
            if slot['deviceName'] != "":
                vp = virtualports
                print("\tDevice: {0:s}".format(slot['deviceName']))
                portnum = 0
                for port in slot['physicalPorts']:
                    wwn = str(port['wwn'])
                    print ("\t\tPort {0:d} {1:s}".format(portnum, wwn))
                    portnum = portnum + 1
of.close()

