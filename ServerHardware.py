# -*- coding: utf-8 -*-
###
# (C) Copyright [2021] Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###
#
# Mac to IPv6 info at https://networklessons.com/ipv6/ipv6-eui-64-explained

from hpeOneView.oneview_client import OneViewClient
from hpeOneView.exceptions import HPEOneViewException
from ConfigLoader import try_load_from_file
import json

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

# ipv62mac - convert a IPv6 address to HW MAC Id
# based on standards
# input = ipv6 address as A:B:C:D:E:F:G:H format
# return = MAC Id as AA:BB:CC:DD:EE:FF format

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

###
# __main__
# Grab info for Synergy Appliance.
# NOTE: THIS USES CLEAR TEXT PASSWORDS!
config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
server_hardwares = oneview_client.server_hardware

# Open a file for the MAC ID information
installJson = "./jsonfiles/MACids.json"
df = open(installJson, 'w')
# Could add a write to the file for column lables, change file to .csv, etc.

# Get list of all server hardware resources
#
# Build a list of any IPv4 addresses found (servers)
# Create a text file with the FrameName, Server Slot and MAC ID
print("Get list of all server hardware Appliance")
server_hardware_all = server_hardwares.get_all()
for serv in server_hardware_all:
    for k, v in serv['mpHostInfo'].items():
        if k == "mpIpAddresses":
            frame = serv['locationUri'].split("/")
            iLO_IP = v[len(v)-1]['address']
            mac = ipv62mac(v[0]['address'])
            location = frame[len(frame)-1]
            outstring = location+','+str(serv['position'])+','+mac+','+iLO_IP
            df.write(outstring)
            df.write('\n')