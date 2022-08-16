# Code to build a dictionary out of a CSV file
# this dictionary is focused on automted installaiton of 
# Synergy blades in a OneView environment
#
# data.cs structure
# iloIP,User,Pass,isoDir,iso,ksTemplate,NewCfg,NewIP,NewHostName,ESXUser,ESXpwd
#
# Notepad ...
# Structure of data needs to ahve
# * Individuall for each server
#   * IP
#   * iLO IP
#   * Hostname
#   * iLO Hostname
#   * dir for kickstart
# * stays the same
#   * ISO location, ISO
#   * Kickstrat file name 
#   * Domain
#
# - could create uniqne names for ks based off IP/Hostname.  Reduces data.csv 
# - could create a file for the non changing data and one for change data
#

import csv
from pprint import pprint
from hpeOneView.oneview_client import OneViewClient
from ConfigLoader import try_load_from_file

def GetServers(dc_info):
    servers = []
    for server in dc_info['server_mpHostsAndRanges']:
        servers.append(server)
    return servers

def ListServers(svrList, *args):
    for s in svrList:
        print(s)

def DCInfo():
    config = {
        "ip": "<oneview_ip>",
        "num_enclosures":"<num_enclosures>",
        "num_hosts":"<num_hosts>",
        "host_names":"<server_hostnames>",
        "encl_names":"<enclosure_names>",
        "credentials": {
            "userName": "<username>",
            "password": "<password>"
        }
    }

    # Try load config from a file (if there is a config file)
    config = try_load_from_file(config)
    # return Data Center info(config)
    return config

### __main__
if __name__ == "__main__":
    dc_config = DCInfo()
#    for applianceIP in (dc_config['enclosure_ip_range']):
#        print("Appliance IP : ",applianceIP)

#    for iloHost in (dc_config['server_mpHostsAndRanges']):
#        print(iloHost)
    svrs = []
    svrs = GetServers(dc_config)
    print ("Now lets call ListServers")
    ListServers(svrs)

    