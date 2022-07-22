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
    "api_version": "<api_version>"
}

def save_file(data_file, outfile, m):
     with open(file=outfile, mode=m) as output_file:
         json.dump(data_file, output_file, indent=5)
 
JSON_DIR = ".\jsonfiles\\"
# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)

# Get configured network interface from appliance
print("Get network interface details from appliance: ")
# network_interface = oneview_client.appliance_network_interfaces
network_interfaces = oneview_client.appliance_network_interfaces.get_all().data['applianceNetworks']
outnames = network_interfaces[0]['hostname']
rootname = outnames.split('.')[0]

# print(rootname)
outfile=JSON_DIR+"appliance_networks.json"
save_file(network_interfaces, outfile,"w")

print("Get Synergy Composer appliance details: ")
appliances = oneview_client.appliance_node_information.get_status()
outfile=JSON_DIR+"appliance.json"
save_file(appliances.data, outfile,"w")

print("Get enclosure and enclosure groups details from appliance: ")
enclosures = oneview_client.enclosures.get_all()
outfile=JSON_DIR+"enclosures.json"
open(outfile,"w")
for enclosure in enclosures:
    save_file(enclosure, outfile,"a+")

egs = oneview_client.enclosure_groups.get_all()
outfile=JSON_DIR+"egs.json"
open(outfile,"w")
#with open(file=outfile, mode="w") as output_file:
for eg in egs:
    save_file(eg, outfile,"a+")

print("Get all the Server Profile Templates and Server Profiles from appliance: ")
spts = oneview_client.server_profile_templates.get_all()
for spt in spts:
    spt_name = (spt['name'])+"_spt_"+".json"
    outfile=JSON_DIR+spt_name
    save_file(spt, outfile,"w")
    
print("Get list of all server profiles")
server_profiles = oneview_client.server_profiles
all_profiles = server_profiles.get_all()
for profile in all_profiles:
    profile_name = (profile['name'])+".json"
    outfile=JSON_DIR+profile_name
    save_file(profile, outfile,"w")

print("Get list of all the servers from appliance: ")
servers = oneview_client.server_hardware.get_all()
outfile=JSON_DIR+"servers.json"
open(outfile,"w")
with open(file=outfile, mode="w") as output_file:
    for svr in servers:
        save_file(svr, outfile,"a+")
        frame = svr['locationUri'].split("/")
        location = frame[len(frame)-1]
        bay = svr['position']
        print("============")
        #pprint(svr['portMap']['deviceSlots'][0]['physicalPorts''interconnectPort'])
        print(location,',',bay,',',svr['portMap']['deviceSlots'][0]['physicalPorts'][0]['wwn'])

print("Get all the defined Networks from appliance: ")
ethernet_networks = oneview_client.ethernet_networks
ethernet_nets_sorted = ethernet_networks.get_all(sort='name:descending')
outfile = JSON_DIR+"networks.json"
open(outfile,"w")
for net in ethernet_nets_sorted:
    save_file(net,outfile,"a+")

fabrics = oneview_client.fabrics.get_all(sort='name:descending')
outfile = JSON_DIR+"fabrics.json"
open(outfile,"w")
for fabric in fabrics:
    save_file(fabric,outfile,"a+")

fc_networks = oneview_client.fc_networks.get_all(sort='name:descending')
outfile = JSON_DIR+"fc_networks.json"
open(outfile,"w")
for fc_network in fc_networks:
    save_file(fc_network,outfile,"a+")

fcoe_networks = oneview_client.fcoe_networks.get_all(sort='name:descending')
outfile = JSON_DIR+"fcoe_networks.json"
open(outfile,"w")
for fcoe_network in fcoe_networks:
    save_file(fcoe_network,outfile,"a+")

# list of more info to inventory
# oneview_client.appliance_network_interfaces
# oneview_client.drive_enclosures
# oneview_client.endpoints
# oneview_client.id_pools_ipv4_ranges
# oneview_client.sas_logical_jbods
# oneview_client.logical_interconnect_groups
# oneview_client.logical_interconnects
# oneview_client.logical_enclosures
# oneview_client.login_details
# oneview_client.managed_sans
# oneview_client.network_sets
# oneview_client.power_devices
# oneview_client.racks
# oneview_client.repositories
# oneview_client.storage_pools
# oneview_client.storage_systems
# oneview_client.storage_volume_templates
# oneview_client.storage_volume_attachments
# oneview_client.unmanaged_devices
# oneview_client.volumes