# pylint: disable=line-too-long

''' -*- coding: utf-8 -*-

 (C) Copyright [2021] Hewlett Packard Enterprise Development LP

 Licensed under the Apache License, Version 2.0 (the 'License');
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an 'AS IS' BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

 This program is used to call the functions used to setup
 synergy frames and servers

-------------------------------------------------------------------------------------------------------
This Python script saves the iLO security settings for all serves in a OneView system
or as given in the -l <file server list file> argument

Requirements
   - HPE OneView Python Library
   - HPE OneView administrator account

Options:
    - file with list of server hostnames AS DEFINED IN the ONEVIEW APPLIANCE

Output sample:

        python.exe save_ilo_security.py -l ilos.txt 
        Change iLO Security settings: [18-08-2022, 11:18:17]
        Make sure OneView host 10.10.106.1 exists ... Success
        D:\Scripts\Python\OneView\python-synergy\Synergy-Python\jsonfiles\ilo_security.json exists. File will be overwritten!
        Saving security settings for iLO Hostname ILOMXQ0350HGP.atlpss.hp.net Addresses 10.10.106.52: 
        Saving security settings for iLO Hostname ILOMXQ0350HGB.atlpss.hp.net Addresses 10.10.106.58: 
        Saving security settings for iLO Hostname ILOMXQ0350HGC.atlpss.hp.net Addresses 10.10.106.59: 
        Saving security settings for iLO Hostname ILOMXQ0350HGQ.atlpss.hp.net Addresses 10.10.106.56: 
        Saving security settings for iLO Hostname ILOMXQ0350HGD.atlpss.hp.net Addresses 10.10.106.50: 
        Saving security settings for iLO Hostname ILOMXQ0350HGH.atlpss.hp.net Addresses 10.10.106.57: 
        Saving security settings for iLO Hostname ILOMXQ0350HGL.atlpss.hp.net Addresses 10.10.106.61: 
        Saving security settings for iLO Hostname ILOMXQ0350HGF.atlpss.hp.net Addresses 10.10.106.51: 
        Saving security settings for iLO Hostname ILOMXQ0350HGM.atlpss.hp.net Addresses 10.10.106.60: 
        Saving security settings for iLO Hostname ILOMXQ0350HGK.atlpss.hp.net Addresses 10.10.106.72:
        Saving security settings for iLO Hostname ILOMXQ0350HGJ.atlpss.hp.net Addresses 10.10.106.75: 
        Saving security settings for iLO Hostname ILOMXQ0350HGG.atlpss.hp.net Addresses 10.10.106.55: 
        Saving security settings for iLO Hostname ILOMXQ0350HGN.atlpss.hp.net Addresses 10.10.106.53: 
        Checked 13 ilos

'''
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
