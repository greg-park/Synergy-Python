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
This Python script compares the iLO security settings against a set of default settings.  If the 
host iLO does not match the default then that particular security setting is changed to match the
default value

Requirements
   - HPE OneView Python Library
   - HPE OneView administrator account

Options:
    - file with list of server hostnames AS DEFINED IN the ONEVIEW APPLIANCE

Output sample:

        Checking security settings for 2-Synergy106-B, bay 2
        No changes on 2-Synergy106-B, bay 2,10.10.106.52
        Checking security settings for 2-Synergy106-B, bay 8
        ***** Mismatch *****
        2-Synergy106-B, bay 8 setting SNMPv1 set to FalseChanged to True
        ilo Security settings changed.  New settings are:
        {  '@odata.context': '/redfish/v1/$metadata#HpeiLOSecurityParam.HpeiLOSecurityParam',
           '@odata.etag': 'W/"A3A6BF43"',
           '@odata.id': '/redfish/v1/Managers/1/SecurityService/SecurityDashboard/SecurityParams/10/',
           '@odata.type': '#HpeiLOSecurityParam.v1_1_0.HpeiLOSecurityParam',
           'Description': 'SNMPv1 is enabled. This configuration increases system '
                          'vulnerability to attack.',
           'Id': '10',
           'Ignore': True,
           'IgnoredBy': '_HPOneViewAdmin',
           'IgnoredTime': '2022-08-18T14:43:37Z',
           'Name': 'SNMPv1',
           'SecurityStatus': 'Risk',
           'State': 'Enabled'}
        Fixed 1 settings on 2-Synergy106-B, bay 8,10.10.106.58
        updated security for 1 servers

Notes:
    This code really does nothing but run rest calls.  It does NOT inventory the iLO settings
    BIOS, etc.
    
'''

import sys
import getopt
import argparse
import json
# import csv
import time
import os.path
import subprocess
import platform
from datetime import datetime
# from fileinput import filename
from pprint import pprint

import requests
from urllib3.exceptions import InsecureRequestWarning

from hpeOneView.oneview_client import OneViewClient
# from tabulate import tabulate
from config_loader import try_load_from_file

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
JSON_DIR = 'jsonfiles'
SERVER_DIR = 'servers'

def usage():
    '''
    usage function
    '''
    print("useage: change_ilo_security.py -h -l <file list> -v")
    print(" -h: help")
    print(" -l: <file containing servernames>")
    print(" -v: verbose")

def get_time_stamp():
    '''
    get_time_stamp function.  Used to mark time during execution
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

def check_security_settings(server_name, objects):
    '''
    Check the security settings for "server_name" vs "objects" and fix 
    any settings that do not match
    '''
    mismatch = 0
    headers = {
        'OData-Version':'4.0',
        'X-Auth-Token':''
    }

    post_data = {
        'Ignore':False
    }

    config= []
    config = try_load_from_file(config)

    # Ensure the OneView/Composer target exists.  If not then exit
    print(f"Checking security settings for {server_name}")
    hostname = config["ip"]
    if ping (config["ip"]) != 0:
        print (f"Host {hostname} not found, exiting program")
        exit(1)
    # else:
    #    print(f"Success Host {hostname} found")

    try:
        oneview_client = OneViewClient(config)
    except Exception as e:
        print('Connect Error:', e)
        exit()

    server = oneview_client.server_hardware.get_by_name(server_name)
    addresses = server.data['mpHostInfo']['mpIpAddresses']
    ilo_ip = addresses[len(addresses)-1]['address']
#
    server_hw = oneview_client.server_hardware.get_by_name(server.data['name'])
    remote_console = server_hw.get_remote_console_url()
    session_id = (remote_console['remoteConsoleUrl']).split("=")[2]
#
#  /redfish/v1/systems/1/
# /redfish/v1/Managers/1/
# 
#
    headers['X-Auth-Token'] = session_id
    rf_call = "/redfish/v1/Managers/1/"
    url = "https://"+ilo_ip+rf_call
    r_security_dashboard = requests.get(url, headers=headers, verify=False)
    print("Return: ", r_security_dashboard.status_code)
    json_security_dashboard = json.loads(r_security_dashboard.content)
    pprint(json_security_dashboard)
    
    return(1)

def get_servers(server_file):
    '''
    docstring
    '''    
    server_list = []
    config= []
    config = try_load_from_file(config)
    # Ensure the OneView/Composer target exists.  If not then exit
    # print("Make sure OneView host exists ... ", end=" ")
    hostname = config["ip"]
    if ping (config["ip"]) != 0:
#        print(f"Success Host {hostname} found")
#    else:
        print (f"Host {hostname} not found, exiting program")
        exit(1)

    try:
        oneview_client = OneViewClient(config)
    except Exception as e:
        print('Connect Error:', e)
        exit()

    if server_file is None:
        servers = oneview_client.server_hardware.get_all()
    else:
        fd = open(server_file, "r")
        for readline in fd:
            server_name = readline.rstrip('\n')
            server_list.append(server_name)

    #for server in servers:
    #    print("Server name: ", server['name'])
    #    server_list.append(server['name'])
    return(server_list)

if __name__ == "__main__":
    argv = sys.argv[1:]  
    try:
        opts, args = getopt.getopt(argv, "hl:v", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    server_file = None
    verbose = False
    for opt, arg in opts:
        if opt in ["-v", "--verbose"]:
            verbose = True
        elif opt in ["-h", "--help"]:
            usage()
            sys.exit()
        elif opt in ["-l", "--list"]:
            server_file = arg
        else:
            assert False, "unhandled option"
    
#

    data_file = os.path.join(os.getcwd(),JSON_DIR, "ilo_gjp.json")
    df = open(data_file, "r")
    security_objects = json.load(df)
    # read_json(security_objects)
    # read_server_json(security_objects)
    server_list = get_servers(server_file)

    changes = 0
    total_changes = 0
    # check_security_settings("1-Synergy106-T, bay 2", security_objects)
    for server in server_list:
        changes = check_security_settings(server, security_objects)
        if changes > 0:
            total_changes = total_changes + 1

    print(f"Saved settings {total_changes} servers")
