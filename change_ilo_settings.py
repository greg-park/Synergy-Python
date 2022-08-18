##############################################################################
# change_iLO_settings.py
# - Script for getting ilo security settings
#
#   VERSION 1.0
#   Date:
#   Input: ilo_security.json, config.json
#   Output: Write to stdout the Enclosure name, bay number and MAC id for iLO
#           for the server in that slot.
#
############################################################################## 

import json
import time
import os.path
import subprocess
import platform
from datetime import datetime
# from fileinput import filename
from pprint import pprint

import requests
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# from ConfigLoader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient
# from tabulate import tabulate
# from collections import OrderedDict
from config_loader import try_load_from_file

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
    '''
    docstring
    '''
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

# ipv62mac - convert a IPv6 address to HW MAC Id
# based on standards
# input = ipv6 address as A:B:C:D:E:F:G:H format
# return = MAC Id as AA:BB:CC:DD:EE:FF format

def ipv62mac(ipv6):
    '''
    docstring
    '''
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
    '''
    get_time_stamp function
    '''
    timestamp = time.time()
    date_time = datetime.fromtimestamp(timestamp)
    str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
    return(str_date_time)

def ping(host):
    '''
    ping function
    '''
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    result = subprocess.Popen(command,stdout=subprocess.PIPE)
    stdout, stderr = result.communicate()
    return (result.returncode)


### MAIN CODE ###
print("Change iLO Security settings: [{}]".format(get_time_stamp()))
config = {}
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

try:
    oneview_client = OneViewClient(config)
except Exception as e:
    print('Connect Error:', e)
    exit()
headers = {
    'OData-Version':'4.0',
    'X-Auth-Token':''
}
post_data = {
    'Ignore':False
}
JSON_DIR = 'jsonfiles'
JSON_FILE = 'ilo_security.json'
data_file = os.path.join(os.getcwd(),JSON_DIR, JSON_FILE)
if os.path.isfile(data_file):
    print('{} exists. File will be overwritten!'.format(data_file))
    jsonFile = open(data_file, "w")
else:
    print('{} not found.  File required to save inf ... exiting'.format(data_file))
    exit()
ilo_count = 0
for server in oneview_client.server_hardware.get_all():
    ilo_count = ilo_count + 1
    server_hw = oneview_client.server_hardware.get_by_name(server['name'])
    addresses = server['mpHostInfo']['mpIpAddresses']
    ilo_ip = addresses[len(addresses)-1]['address']
    print("Saving security settings for iLO Hostname {} Addresses {}: ".format(server['mpHostInfo']['mpHostName'], ilo_ip))

    remote_console = server_hw.get_remote_console_url()
    session_id = (remote_console['remoteConsoleUrl']).split("=")[2]
    headers['X-Auth-Token'] = session_id
    rf_call = "/redfish/v1/Managers/1/SecurityService/SecurityDashboard/SecurityParams/"
    url = "https://"+ilo_ip+rf_call
    r_security_dashboard = requests.get(url, headers=headers, verify=False)
    json_security_dashboard = json.loads(r_security_dashboard.content)
#    pprint(json_security_dashboard)

    for member in json_security_dashboard['Members']:
        url = "https://"+ilo_ip+member['@odata.id']
        r_member = requests.get(url, headers=headers, verify=False)
        json_member = json.loads(r_member.content)
#        pprint(json_member)
        json.dump(json_member, jsonFile)
        #if json_member['Name'] == "Minimum Password Length":
        #    pprint(json_member)
        #    r_member = requests.patch(url, json=post_data, headers=headers, verify=False)
        #    r_check= requests.get(url, headers=headers, verify=False)

print("Checked {} ilos".format(ilo_count))
jsonFile.close()
