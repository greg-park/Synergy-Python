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
'''

        "/controller-state.json":'controller-state',
        "/rest/appliance/configuration/time-locale":'time-locale',
        "/rest/appliance/device-read-community-string":'device-read-community-string',
        "/rest/appliance/eula/status":'eula-status',
        "/rest/appliance/firmware/notification":'firmware-notification',
        "/rest/appliance/firmware/pending":'firmware-pending',
        "/rest/appliance/firmware/verificationKey":'firmware-verificationkey',
        "/rest/appliance/ha-nodes":'ha-nodes',
        "/rest/appliance/health-status":'health-status',
        "/rest/appliance/network-interfaces":'network-interfaces',
        "/rest/appliance/network-interfaces/mac-addresses":'network-interfaces-mac',
        "/rest/appliance/nodeinfo/status":'nodeinfo-status',
        "/rest/appliance/nodeinfo/version":'nodeinfo-version',
        "/rest/appliance/notifications/email-config":'notification-email-config',
        "/rest/appliance/notifications/test-email-config":'notification-test-email-config',
        "/rest/appliance/progress":'progress',
        "/rest/appliance/proxy-config":'proxy-config',
        "/rest/appliance/settings/serviceaccess":'settings-serviceaccess',
        "/rest/appliance/snmpv3-trap-forwarding/destinations":'snmpv3-destinations',
        "/rest/appliance/snmpv3-trap-forwarding/users":'snmpv3-users',
        "/rest/appliance/ssh-access": 'ssh-access',
        "/rest/appliance/static-routes":'static-routes',
        "/rest/appliance/trap-destinations":'trap-destinations'
    }


appliance_settings :{
        "/rest/backups":'backups',
        "/rest/backups/config":'backups-config',
        "/rest/deployment-servers/image-streamer-appliances":'image-streamer-appliances',
        "/rest/domains":'domains',
        "/rest/domains/schema":'domains-schema',
        "/rest/firmware-drivers":'firmware-drivers',
        "/rest/global-settings":'global-settings',
        "/rest/hardware-compliance":'hardware-compliance',
        "/rest/hw-appliances":'hw-appliances',
#         "/rest/index/resources?query=`"NOT scopeUris:NULL`"", 'scopes-resources',
        "/rest/licenses":'licenses',
        "/rest/remote-syslog":'remote-syslog',
        "/rest/repositories":'repositories',
        "/rest/restores":'restores',
        "/rest/scopes":'scopes',
        "/rest/updates":'updates',
        "/rest/update-settings/schedule":'update-settings-schedule',
        "/rest/version":'version'
    }

'''

import sys
import json
import time
import subprocess
import platform
import argparse

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

class gjp_class():
    SessionDict = {
        "login":"rest/login-sessions"
    }
    ApplianceDict = {
        'controller-state':"/rest/appliance/controller-state.json",
        'time-locale':"/rest/appliance/configuration/time-locale",
        'device-read-community-string':"/rest/appliance/device-re,ad-community-string",
        'eula-status':"/rest/appliance/eula/status",
        'firmware-notification':"/rest/appliance/firmware/notification",
        'firmware-pending':"/rest/appliance/firmware/pending",
        'firmware-verificationkey':"/rest/appliance/firmware/verificationKey",
        'ha-nodes':"/rest/appliance/ha-nodes",
        'health-status':"/rest/appliance/health-status",
        'network-interfaces':"/rest/appliance/network-interfaces",
        'network-interfaces-mac':"/rest/appliance/network-interfa,ces/mac-addresses",
        'nodeinfo-status':"/rest/appliance/nodeinfo/status",
        'nodeinfo-version':"/rest/appliance/nodeinfo/version",
        'notification-email-config':"/rest/appliance/notifications/email-config",
        'notification-test-email-config':"/rest/appliance/notifications/test-email-config",
        'progress':"/rest/appliance/progress",
        'proxy-config':"/rest/appliance/proxy-config",
        'settings-serviceaccess':"/rest/appliance/settings/serviceaccess",
        'snmpv3-destinations':"/rest/appliance/snmpv3-trap-forwarding/destinations",
        'snmpv3-users':"/rest/appliance/snmpv3-trap-forwarding/users",
         'ssh-access':"/rest/appliance/ssh-access",
        'static-routes':"/rest/appliance/static-routes",
        'trap-destinations':"/rest/appliance/trap-destinations",
        'backups':"/rest/backups",
        'backups-config':"/rest/backups/config",
        'image-streamer-appliances':"/rest/deployment-servers/image-streamer-appliances",
        'domains':"/rest/domains",
        'domains-schema':"/rest/domains/schema",
        'firmware-drivers':"/rest/firmware-drivers",
        'global-settings':"/rest/global-settings",
        'hardware-compliance':"/rest/hardware-compliance",
        'hw-appliances':"/rest/hw-appliances",
#        NULL`"", 'scopes-resources',	# : "/rest/index/resource,s?query=`"NOT scopeUris
        'licenses':"/rest/licenses",
        'remote-syslog':"/rest/remote-syslog",
        'repositories':"/rest/repositories",
        'restores':"/rest/restores",
        'scopes':"/rest/scopes",
        'updates':"/rest/updates",
        'update-settings-schedule':"/rest/update-settings/schedule",
        'version':"/rest/version"
    }

    headers = {
        'Content-Type': 'application/json',
        'X-Api-Version': '4200'
    }
    post_headers = {
        'Content-Type': 'application/json',
        'X-Api-Version': '4200'
    }

    body = { 
        'authLoginDomain': "local", 
        'userName': "Administrator", 
        'password': "HP1nvent"
    }
    app = "10.10.10.1"
    call = "put"

    def __init__(self, s):
        self.string = s
    def __call__(self):
        print(self.string)

    def class_postCall(self, post):
        resp = None
        body = self.body
        uri = "https://{}/{}/".format(self.app, self.SessionDict[post])
        print("POST: ", uri)

        try:
            resp = requests.post(uri, headers=self.post_headers, data=json.dumps(body), verify=False)
            if (resp.status_code != 200):
                print("OV Connection ..... Failed: ", resp.status_code)
        except Exception as e:
            print(f"Unable to reach OneView appliance. Reason  - {e}.")
            print("OV Connection ..... Failed: ",resp.status_code)
        return resp.json()
# End of class

def getCall(local_s, call, getVersion, getSession):
    resp = None
    uri = "https://{}{}".format(local_s.app, local_s.ApplianceDict[call])
    print("GET: ", uri)
    if getSession == "" :
        get_headers = local_s.headers
    else:
        get_headers = {
            'Content-Type': 'application/json',
            'X-Api-Version': str(getVersion),
            'Auth':getSession
        }

    print (get_headers)
# pass into the function the call and the ovAppliance
    try:
        resp = requests.get(uri,headers=get_headers, verify=False)
    except Exception as e:
            print(f"Unable to reach OV Appliance. Reason  - {e}.")
            print(f"OV Get call ..... Failed:{resp.status_code}")

#    pprint(json.loads(resp.content))
    return resp.json()


def postCall(post_s, post):
    resp = None
    body = post_s.body
    uri = "https://{}/{}/".format(post_s.app, post_s.SessionDict[post])
    print("POST: ", uri)

    try:
        resp = requests.post(uri, headers=post_s.post_headers, data=json.dumps(body), verify=False)
        if (resp.status_code != 200):
            print("OV Connection ..... Failed: ", resp.status_code)
    except Exception as e:
        print("Unable to reach OneView appliance. Reason  - {}.".format(e))
        print("OV Connection ..... Failed: ",resp.status_code)
    return resp.json()

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

#

if __name__ == "__main__":

    # Initialize parser
    parser = argparse.ArgumentParser(description = "Script to inventory OneView Appliance")

    parser.add_argument(
        '-d',
        '--destination',
        dest='comp_path',
        action="store",
        required=False,
        help="The path to the destination directory",
        default=None)
    parser.add_argument(
        '-o',
        '--ovhost',
        dest='ov_host',
        action="store",
        required=False,
        help="IP of the OneView Appliance",
        default=None)
    parser.add_argument(
        '-u',
        '--user',
        dest='ov_user',
        action="store",
        required=False,
        help="OneView username to login",
        default=None)
    parser.add_argument(
        '-p',
        '--password',
        dest='ov_pass',
        action="store",
        required=False,
        help="OneView password to log in.",
        default=None)

    options = parser.parse_args()

    print (">> ",options.comp_path)
    s1 = gjp_class('Hello')
    s1()
    s1.app = options.ov_host
    post_json = s1.class_postCall("login")
    # post_json = postCall(s1,"login")
    pprint(post_json)
    get_json = getCall(s1,"version","","")
    pprint(get_json)
    print(get_json['currentVersion'])
    
    get_json = getCall(s1, "global-settings", get_json['currentVersion'], post_json['sessionID'])
    pprint(get_json)
