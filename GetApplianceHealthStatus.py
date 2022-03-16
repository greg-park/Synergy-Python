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

# GJP updates.  Change to "main" that calls as a function
#      -  Added check to ensure appliance settings match expected data

from pprint import pprint
from hpeOneView.oneview_client import OneViewClient
from ConfigLoader import try_load_from_file
import platform    # For getting the operating system name
import subprocess  # For executing a shell command

# Check Appliance Health (Appliance IP, username, password)
def appliance_health(config):

    print("Check appliance : ", config['ip'])
    if ping(config['ip']):
        print("Enclosure IP is up!")
        oneview_client = OneViewClient(config)
        app_health = oneview_client.appliance_health_status
        print("\nGet health status information from appliance:\n ")
        return app_health.get_health_status()
    else:
        print("Enclosure not found or not healthy!")
        app_health = None
        return app_health

def ping(host_or_ip, packets=1, timeout=1000):
    if platform.system().lower() == 'windows':
        command = ['ping', '-n', str(packets), '-w', str(timeout), host_or_ip]
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, creationflags=0x08000000)
        return result.returncode == 0 and b'TTL=' in result.stdout
    else:
        command = ['ping', '-c', str(packets), '-w', str(timeout), host_or_ip]
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0

### __main__
if __name__ == "__main__":
    appliance = appliance_health()
    if appliance:
        print("Success!")
    else:
        print("Error creating enclosure and Data Center info")