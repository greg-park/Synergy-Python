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

get_iLO_settings.py
- Script for getting ilo security settings
  VERSION 1.0
  Date:
  Input: config.json
  Output: Write to stdout the Enclosure name, bay number and MAC id for iLO
          for the server in that slot.
'''

import sys
import getopt
import json
import csv
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

from hpeOneView.oneview_client import OneViewClient
# from tabulate import tabulate
from config_loader import try_load_from_file

JSON_DIR = 'jsonfiles'
SERVER_DIR = 'servers'
JSON_FILE = '1-Synergy106-T_bay_1.json'
# .\jsonfiles\servers\1-Synergy106-T_bay_1.json

def usage():
    print("useage: get_ilo_security.py -h -l <file list> -v")

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

def check_ilo_security():
    '''
    docstring
    '''

    argv = sys.argv[1:]
    servers = []

    headers = {
        'OData-Version':'4.0',
        'X-Auth-Token':''
    }
    post_data = {
        'Ignore':False
    }
  
    try:
        opts, args = getopt.getopt(argv, "hl:v", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    in_list = None
    verbose = False
    for opt, arg in opts:
        if opt in ["-v", "--verbose"]:
            verbose = True
        elif opt in ["-h", "--help"]:
            usage()
            sys.exit()
        elif opt in ["-l", "--list"]:
            in_list = arg
        else:
            assert False, "unhandled option"

###
    print("Change iLO Security settings [{}]".format(get_time_stamp()))
    config = {}
    config = try_load_from_file(config)

    # Ensure the OneView/Composer target exists.  If not then exit
    print("Make sure OneView host exists ... ", end=" ")
    hostname = config["ip"]
    if ping (config["ip"]) == 0:
        print(f"Success Host {hostname} found")
    else:
        print (f"Host {hostname} not found, exiting program")
        exit(1)

    try:
        oneview_client = OneViewClient(config)
    except Exception as e:
        print('Connect Error:', e)
        exit()

    if in_list:
        data_file = os.path.join(os.getcwd(),in_list)
        print ("Checking: ", data_file)
        if os.path.isfile(data_file):
            print("Found the file")
            with open(data_file, "r") as file:
#                nl_break = ""
                for readline in file:
                    server_name = readline.rstrip('\n')
                    tserver = oneview_client.server_hardware.get_by_name(server_name)
                    servers.append(tserver.data)
    else:
        servers = oneview_client.server_hardware.get_all()

    ilo_count = 0
    for server in servers:
        ilo_count = ilo_count + 1
        addresses = server['mpHostInfo']['mpIpAddresses']
        ilo_ip = addresses[len(addresses)-1]['address']
        ilo_hostname = server['mpHostInfo']['mpHostName']
        print("{},{},{}".format(server['name'],ilo_hostname, ilo_ip))
        server_hw = oneview_client.server_hardware.get_by_name(server['name'])
        remote_console = server_hw.get_remote_console_url()
        session_id = (remote_console['remoteConsoleUrl']).split("=")[2]
# 
        headers['X-Auth-Token'] = session_id
        rf_call = "/redfish/v1/Managers/1/SecurityService/SecurityDashboard/SecurityParams/"
        url = "https://"+ilo_ip+rf_call
        r_security_dashboard = requests.get(url, headers=headers, verify=False)
        json_security_dashboard = json.loads(r_security_dashboard.content)
        # pprint(json_security_dashboard)
# 
        for member in json_security_dashboard['Members']:
            url = "https://"+ilo_ip+member['@odata.id']
            r_member = requests.get(url, headers=headers, verify=False)
            json_member = json.loads(r_member.content)
            pprint(json_member)
    #         json.dump(json_member, jsonFile)
    #         #if json_member['Name'] == "Minimum Password Length":
    #         #    pprint(json_member)
    #         #    r_member = requests.patch(url, json=post_data, headers=headers, verify=False)
    #         #    r_check= requests.get(url, headers=headers, verify=False)
# 
    print("Checked {} ilos".format(ilo_count))

# End

if __name__ == "__main__":
    check_ilo_security()
