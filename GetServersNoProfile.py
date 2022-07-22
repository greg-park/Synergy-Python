# Simple set of loops to inventory a Synergy/OneView environment
#
# Easily consumable by others
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
    "profile_name": "<profile_name>",
    "api_version": "<api_version>"
}

def save_file(data_file, outfile, m):
     with open(file=outfile, mode=m) as output_file:
         json.dump(data_file, output_file, indent=5)
 
JSON_DIR = ".\jsonfiles\\"
# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)

# print("Get all the Server Profile Templates and Server Profiles from appliance: ")
# spts = oneview_client.server_profile_templates.get_all()
# for spt in spts:
#    spt_name = (spt['name'])+"_spt_"+".json"
#    outfile=JSON_DIR+spt_name
#    save_file(spt, outfile,"w")
    
#print("Get list of all server profiles")
#server_profiles = oneview_client.server_profiles
#all_profiles = server_profiles.get_all()
#for profile in all_profiles:
#    profile_name = (profile['name'])+".json"
#    outfile=JSON_DIR+profile_name
#    save_file(profile, outfile,"w")
NoProfileServers = []
ProfileServers = []
count = 0

print("Get list of all the servers from appliance: ")
servers = oneview_client.server_hardware.get_all()
# outfile=JSON_DIR+"servers.json"
# open(outfile,"w")
#with open(file=outfile, mode="w") as output_file:

server_profiles = oneview_client.server_profiles
Test = server_profiles.get_all()

print("Frame            bay")
for svr in servers:
    frame = svr['locationUri'].split("/")
    location = frame[len(frame)-1]
    bay = str(svr['position'])
    profile = location+'_'+str(bay)+'_'+config['profile_name']
    if svr['state'] == "NoProfileApplied":
        NoProfileServers.append(svr)
    else:
        ProfileServers.append(svr)

print("These servers do not have profiles")
for s in NoProfileServers:
    print ("{0:s} {1:s}\t{2:s}".format(location,bay,profile))

print("Servers that do have profiles")
for s in ProfileServers:
    #pprint(s['name'], location, bay)
    pprint(s['name'])
