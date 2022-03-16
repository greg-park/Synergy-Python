# Copyright 2020 Hewlett Packard Enterprise Development LP
 #
 # Licensed under the Apache License, Version 2.0 (the "License"); you may
 # not use this file except in compliance with the License. You may obtain
 # a copy of the License at
 #
 #      http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 # WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 # License for the specific language governing permissions and limitations
 # under the License.

# -*- coding: utf-8 -*-
"""
An example of mounting virtual media for HPE iLO systems
"""

import sys
import json
from redfish import RedfishClient
from redfish.rest.v1 import ServerDownOrUnreachableError
from get_resource_directory import get_resource_directory
import ReadDataDict

# Mount_Virtual_Media_ISO Function
# This is pulled from the HPE iLO Redfish examples
#
def mount_virtual_media_iso(_redfishobj, iso_url, media_type, boot_on_next_server_reset, DISABLE_RESOURCE_DIR):
    virtual_media_uri = None
    virtual_media_response = []
    resource_instances = get_resource_directory(_redfishobj)
    
    if DISABLE_RESOURCE_DIR or not resource_instances:
        managers_uri = _redfishobj.root.obj['Managers']['@odata.id']
        managers_response = _redfishobj.get(managers_uri)
        managers_members_uri = next(iter(managers_response.obj['Members']))['@odata.id']
        managers_members_response = _redfishobj.get(managers_members_uri)
        virtual_media_uri = managers_members_response.obj['VirtualMedia']['@odata.id']
    else:
        for instance in resource_instances:
            if '#VirtualMediaCollection.' in instance['@odata.type']:
                virtual_media_uri = instance['@odata.id']

    if virtual_media_uri:
        virtual_media_response = _redfishobj.get(virtual_media_uri)
        for virtual_media_slot in virtual_media_response.obj['Members']:
            data = _redfishobj.get(virtual_media_slot['@odata.id'])
            if media_type in data.dict['MediaTypes']:
                virtual_media_mount_uri = data.obj['Actions']['#VirtualMedia.InsertMedia']['target']
                post_body = {"Image": iso_url}
                if iso_url:
                    resp = _redfishobj.post(virtual_media_mount_uri, post_body)
                    if boot_on_next_server_reset is not None:
                        patch_body = {}
                        patch_body["Oem"] = {"Hpe": {"BootOnNextServerReset": boot_on_next_server_reset}}
                        boot_resp = _redfishobj.patch(data.obj['@odata.id'], patch_body)
                        if not boot_resp.status == 200:
                            sys.stderr.write("Failure setting BootOnNextServerReset")
                    if resp.status == 400:
                        try:
                            print(json.dumps(resp.obj['error']['@Message.ExtendedInfo'], indent=4, sort_keys=True))
                        except Exception as excp:
                            sys.stderr.write("A response error occurred, unable to access iLO"
                                             "Extended Message Info...")
                    elif resp.status != 200:
                        sys.stderr.write("An http response of \'%s\' was returned.\n" % resp.status)
                break

def unmount_virtual_media_iso(_redfishobj, iso_url, media_type, boot_on_next_server_reset, DISABLE_RESOURCE_DIR):
    virtual_media_uri = None
    virtual_media_response = []

    resource_instances = get_resource_directory(_redfishobj)
    if DISABLE_RESOURCE_DIR or not resource_instances:
        managers_uri = _redfishobj.root.obj['Managers']['@odata.id']
        managers_response = _redfishobj.get(managers_uri)
        managers_members_uri = next(iter(managers_response.obj['Members']))['@odata.id']
        managers_members_response = _redfishobj.get(managers_members_uri)
        virtual_media_uri = managers_members_response.obj['VirtualMedia']['@odata.id']
    else:
        for instance in resource_instances:
            if '#VirtualMediaCollection.' in instance['@odata.type']:
                virtual_media_uri = instance['@odata.id']
 
    if virtual_media_uri:
        virtual_media_response = _redfishobj.get(virtual_media_uri)
        for virtual_media_slot in virtual_media_response.obj['Members']:
            data = _redfishobj.get(virtual_media_slot['@odata.id'])
            if data.obj['Inserted']:
                if media_type in data.dict['MediaTypes']:
                    virtual_media_mount_uri = data.obj['Actions']['#VirtualMedia.EjectMedia']['target']
                    post_body = {}
                    resp = _redfishobj.post(virtual_media_mount_uri, post_body)
                    patch_body = {}
                    patch_body["Oem"] = {"Hpe": {"BootOnNextServerReset": boot_on_next_server_reset}}
                    patch_body["Oem"] = {"Hpe": {"#HpeiLOVirtualMedia.EjectVirtualMedia":['target']}}
                    boot_resp = _redfishobj.patch(data.obj['@odata.id'], patch_body)

def MountServerISO(server, username, password, isopath, action):
    SYSTEM_URL = server
    LOGIN_ACCOUNT = username
    LOGIN_PASSWORD = password
    MEDIA_URL = isopath # Pass full http path and OS image to boot
    MEDIA_TYPE = "CD" #current possible options: Floppy, USBStick, CD, DVD
    BOOT_ON_NEXT_SERVER_RESET = True
    DISABLE_RESOURCE_DIR = False
    try:
        # Create a Redfish client object
        REDFISHOBJ = RedfishClient(base_url=SYSTEM_URL, username=LOGIN_ACCOUNT, password=LOGIN_PASSWORD)
        # Login with the Redfish client
        REDFISHOBJ.login()
    except ServerDownOrUnreachableError as excp:
        sys.stderr.write("ERROR: server not reachable or does not support RedFish.\n")
        sys.exit()

    if action == "mount":
        mount_virtual_media_iso(REDFISHOBJ, MEDIA_URL, MEDIA_TYPE, BOOT_ON_NEXT_SERVER_RESET, DISABLE_RESOURCE_DIR)
    else:
        unmount_virtual_media_iso(REDFISHOBJ, MEDIA_URL, MEDIA_TYPE, BOOT_ON_NEXT_SERVER_RESET, DISABLE_RESOURCE_DIR)
#     REDFISHOBJ.logout()

# Main program is for testing.  Include this for python code access
# Mian
if __name__ == "__main__":
    server = "10.10.108.52"
    username = "hpadmin"
    password = "atlpresales"
    isopath = "http://10.10.108.20/ISO/CentOS-8.5.2111-x86_64-dvd1.iso"
    action = 'mount'
    MountServerISO(server, username, password, isopath, action )