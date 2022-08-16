##############################################################################
# GetiLOMAC.py
# - Script for listing the ilo MAC ids
#
#   VERSION 1.0
#   Date:
#   Input: config.json
#   Output: Write to stdout the Enclosure name, bay number and MAC id for iLO
#           for the server in that slot.
#           - add .csv file in json directory 
#
############################################################################## 
import time
import os.path
import subprocess
import platform
import csv
from datetime import datetime
from hpeOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

# from fileinput import filename
# from pprint import pprint
# from tabulate import tabulate

# Functions used for program
#
# code adapted from https://stackoverflow.com/questions/37140846/how-to-convert-ipv6-link-local-address-to-mac-address-in-python
# for the conversion process check https://nettools.club/mac2ipv6 
#
# mac2ipv6 - convert a HW MAC Id to a IPv6 address 
# based on standards
# input = macID in AA:BB:CC:DD:EE:FF format
# return = IPv6 address as link local (fe80) address

def mac2ipv6(mac):
    parts = mac.split(":")
    parts.insert(3, "ff")
    parts.insert(4, "fe")
    parts[0] = "%x" % (int(parts[0], 16) ^ 2)

    # format output
    ipv6Parts = []
    for i in range(0, len(parts), 2):
        ipv6Parts.append("".join(parts[i:i+2]))
    ipv6 = "fe80::%s/64" % (":".join(ipv6Parts))
    return ipv6

def ipv62mac(ipv6):
    # remove subnet info if given
    subnetIndex = ipv6.find("/")
    if subnetIndex != -1:
        ipv6 = ipv6[:subnetIndex]

    ipv6Parts = ipv6.split(":")
    macParts = []
    for ipv6Part in ipv6Parts[-4:]:
        while len(ipv6Part) < 4:
            ipv6Part = "0" + ipv6Part
        macParts.append(ipv6Part[:2])
        macParts.append(ipv6Part[-2:])

    # modify parts to match MAC value
    macParts[0] = "%02x" % (int(macParts[0], 16) ^ 2)
    del macParts[4]
    del macParts[3]

    return ":".join(macParts)

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

print("Get list of all the servers iLO MAC from OneView appliance [{}]".format(get_time_stamp()))

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>",
    },
    "api_version": "<api_version>"
}
header = ['frame','bay','mac_id','ilo_ip']

# Keep track of data in jsonfiles directory
JSON_DIR = "./jsonfiles"
OUTFILE = "ilos.csv"
data_file = os.path.join(os.getcwd(),JSON_DIR, OUTFILE)

if os.path.isfile(data_file):
    print('{} exists. File will be overwritten!'.format(data_file))
    outfile = open(data_file, 'w', encoding='UTF8', newline='')
else:
    print('{} not found.  File required to save inf ... exiting'.format(data_file))
    exit()

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
enclosure_resource = oneview_client.enclosures
profiles = []
totalMAC = 0

for server in servers:
    enclosure = enclosure_resource.get_by_uri(server['locationUri'])
    for k, v in server['mpHostInfo'].items():
        if k == "mpIpAddresses":
            totalMAC = totalMAC+1
            iLO_IP = v[len(v)-1]['address']
            mac = ipv62mac(v[0]['address'])
# Save the data in a dict to sort
            pDict = {'name':enclosure.data['name'], 'bay':server['position'], 'mac':mac,'ilo_ip': iLO_IP}
            profiles.append(pDict)
print("Total iLO MAC ids: ",totalMAC)
##

# Sort data on enclosure name and bay
profiles.sort(key=lambda x: (x['name'],x['bay'],x['mac']))
writer = csv.writer(outfile)
writer.writerow(header)
for p in profiles:
    outstr = (p['name'],str(p['bay']),str(p['mac']),str(p['ilo_ip']))
    writer.writerow(outstr)

outfile.close()

