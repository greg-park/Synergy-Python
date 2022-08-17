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

 Just a place to test python examples
'''
# output_dict = {
#   '/controller-state.json':'controller-state.txt'
#   '/rest/appliance/configuration/time-locale':'time-locale.txt',
#   '/rest/appliance/device-read-community-string', 'device-read-community-string.txt',
#   '/rest/appliance/eula/status':'eula-status.txt',
#   '/rest/appliance/firmware/notification':'firmware-notification.txt',
#   '/rest/appliance/firmware/pending':'firmware-pending.txt',
#   '/rest/appliance/firmware/verificationKey':'firmware-verificationkey.txt',
#   '/rest/appliance/ha-nodes':'ha-nodes.txt',
#   '/rest/appliance/health-status':'health-status.txt',
#   '/rest/appliance/network-interfaces':'network-interfaces.txt',
#   '/rest/appliance/network-interfaces/mac-addresses', 'network-interfaces-mac.txt',
#   '/rest/appliance/nodeinfo/status':'nodeinfo-status.txt',
#   '/rest/appliance/nodeinfo/version':'nodeinfo-version.txt',
#   '/rest/appliance/notifications/email-config','notification-email-config.txt',
#   '/rest/appliance/notifications/test-email-config':'notification-test-email-config.txt',
#   '/rest/appliance/progress':'progress.txt',
#   '/rest/appliance/proxy-config': 'proxy-config.txt',
#   '/rest/appliance/settings/serviceaccess':'settings-serviceaccess.txt',
#   '/rest/appliance/snmpv3-trap-forwarding/destinations', 'snmpv3-destinations.txt',
#   '/rest/appliance/snmpv3-trap-forwarding/users': 'snmpv3-users.txt',
#   '/rest/appliance/ssh-access':'ssh-access.txt',
#   '/rest/appliance/static-routes': 'static-routes.txt',
#   '/rest/appliance/trap-destinations':'trap-destinations.txt',
#   '/rest/backups': 'backups.txt',
#   '/rest/backups/config':'backups-config.txt',
#   '/rest/deployment-servers/image-streamer-appliances',  'image-streamer-appliances.txt',
#   '/rest/domains':'domains.txt',
#   '/rest/domains/schema':'domains-schema.txt',
#   '/rest/firmware-drivers':'firmware-drivers.txt',
#   '/rest/global-settings':'global-settings.txt',
#   '/rest/hardware-compliance':'hardware-compliance.txt',
#   '/rest/hw-appliances':'hw-appliances.txt',
#   '/rest/licenses': 'licenses.txt',
#   '/rest/remote-syslog':'remote-syslog.txt',
#   '/rest/repositories':'repositories.txt',
#   '/rest/restores':'restores.txt',
#   '/rest/scopes': :'scopes.txt',
#   '/rest/updates'::'updates.txt',
#   '/rest/update-settings/schedule':'update-settings-schedule.txt',
#   '/rest/version':'version.txt'
# }

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
    server = []

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
    print("Change iLO Security settings")
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
    #    pprint(json_security_dashboard)
# 
    #     for member in json_security_dashboard['Members']:
    #         url = "https://"+ilo_ip+member['@odata.id']
    #         r_member = requests.get(url, headers=headers, verify=False)
    #         json_member = json.loads(r_member.content)
    # #        pprint(json_member)
    #         json.dump(json_member, jsonFile)
    #         #if json_member['Name'] == "Minimum Password Length":
    #         #    pprint(json_member)
    #         #    r_member = requests.patch(url, json=post_data, headers=headers, verify=False)
    #         #    r_check= requests.get(url, headers=headers, verify=False)
# 
    # print("Checked {} ilos".format(ilo_count))

def read_json(objects):

    data_file = os.path.join(os.getcwd(),JSON_DIR, "default_security.json")
    df = open(data_file, "r")
    default_security_object = json.load(df)

    for m in default_security_object:
        print("Template member: ",m['@odata.id'])
        print("Template value: ", m['Ignore'])

        for security_object in objects:
            # print("Test value: ", security_object['@odata.id'])
            if security_object['@odata.id'] == m['@odata.id']:
                print("Testing member: ", m['Ignore'], end="")
                print("... against: ", security_object['Ignore'])
                if security_object['Ignore'] == m['Ignore']:
                    print("They match")

def read_server_json(objects):
    '''
    docstring
    '''    
    
    servers = []
    config = []

    headers = {
        'OData-Version':'4.0',
        'X-Auth-Token':''
    }

    post_data = {
        'Ignore':False
    }

    print(f"Check iLO Security settings [{get_time_stamp()}]")

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

    servers = oneview_client.server_hardware.get_all()

    ilo_count = 0
    for server in servers:
        print("Check: ", server['name'])
        ilo_count = ilo_count + 1

        addresses = server['mpHostInfo']['mpIpAddresses']
        ilo_ip = addresses[len(addresses)-1]['address']
        ilo_security_json_file = server['name'].replace(' ',"").replace(',',"_")
        ilo_security_json_file = ilo_security_json_file + "_ilo"+".json"
        # Double check that the server directory exists
        
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
            
            for security_object in objects:
                if security_object['@odata.id'] == member['@odata.id']:
                    print("Test value: ", security_object['@odata.id'])
                    if security_object['Ignore'] != json_member['Ignore']:
                        print("==================== Mismatch ====================")
                        r_member = requests.patch(url, json=post_data, headers=headers, verify=False)
                        r_check= requests.get(url, headers=headers, verify=False)
                        print("ilo Security settings changed ...")
                        pprint(json.loads(r_check.content))

    return()
'''
For server in serverlist:
    if !checkSecuritySettings(server, default_settings):
        changeSettings(server)
'''
def check_security_settings(server_name, objects):
    '''
    docstring
    '''    

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

    server = oneview_client.server_hardware.get_by_name(server_name)
    addresses = server.data['mpHostInfo']['mpIpAddresses']
    ilo_ip = addresses[len(addresses)-1]['address']
    print(f"{server.data['mpHostInfo']['mpHostName']} {ilo_ip}")
#        
    server_hw = oneview_client.server_hardware.get_by_name(server.data['name'])
    remote_console = server_hw.get_remote_console_url()
    session_id = (remote_console['remoteConsoleUrl']).split("=")[2]
##
    headers['X-Auth-Token'] = session_id
    rf_call = "/redfish/v1/Managers/1/SecurityService/SecurityDashboard/SecurityParams/"
    url = "https://"+ilo_ip+rf_call
    r_security_dashboard = requests.get(url, headers=headers, verify=False)
    json_security_dashboard = json.loads(r_security_dashboard.content)
    # pprint(json_security_dashboard)
    for member in json_security_dashboard['Members']:
        url = "https://"+ilo_ip+member['@odata.id']
        r_member = requests.get(url, headers=headers, verify=False)
        json_member = json.loads(r_member.content)
        
        for security_object in objects:
            if security_object['@odata.id'] == member['@odata.id']:
                print("Test value: ", security_object['@odata.id'])
                if security_object['Ignore'] != json_member['Ignore']:
                    print("==================== Mismatch ====================")
                    r_member = requests.patch(url, json=post_data, headers=headers, verify=False)
                    r_check= requests.get(url, headers=headers, verify=False)
                    print("ilo Security settings changed ...")
                    pprint(json.loads(r_check.content))
    return()

def get_servers(server_file):
    '''
    docstring
    '''    
    server_list = []
    config= []
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

    # check_security_settings("1-Synergy106-T, bay 2", security_objects)
    for server in server_list:
        check_security_settings(server, security_objects)