# Simple set of loops to inventory a Synergy/OneView environment
#
###

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
    "api_version": "<api_version>"
}

def save_file(data_file, outfile, m):
     with open(file=outfile, mode=m) as output_file:
         json.dump(data_file, output_file, indent=5)
 
JSON_DIR = ".\jsonfiles\\"
# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
 
print("Get list of all the server MAC IDs from appliance: ")
servers = oneview_client.server_hardware.get_all()
outfile=JSON_DIR+"serverMAC.json"
open(outfile,"w")
with open(file=outfile, mode="w") as output_file:
    for svr in servers:
        save_file(svr, outfile,"a+")
        frame = svr['locationUri'].split("/")
        location = frame[len(frame)-1]
        bay = svr['position']
        macID = location + ',' + str(bay) + ',' + svr['portMap']['deviceSlots'][0]['physicalPorts'][0]['wwn']
        print(macID)

