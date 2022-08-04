##############################################################################
# import_spy.py
# - Script for importing SPT to OneView.
#
#   VERSION 1.0
#   Date:
#   Input: config.json, spts.csv
#       config.json contains the list of variables used
#       spts.csv is just a file with a single line for each SPT json file.
#           The program does verify that file exists before attempting  
#           to read the json data
#   Output: None
#
##############################################################################
import time
import os.path
import subprocess
import platform
import json

# from fileinput import filename
from config_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient
from datetime import datetime

def get_time_stamp():
    timestamp = time.time()
    date_time = datetime.fromtimestamp(timestamp)
    str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
    return(str_date_time)

def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    result = subprocess.Popen(command,stdout=subprocess.PIPE)
    stdout, stderr = result.communicate()
    return (result.returncode)

print("Import Server Profile Templates from json files [{}]".format(get_time_stamp()))

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>",
    },
    "api_version": "<api_version>"
}

# Keep track of data in jsonfiles directory
JSON_DIR = "./jsonfiles"
# Make sure that directory exists
print("Make sure {} exists for data.  Path check = {}".
    format(JSON_DIR, os.path.isdir(JSON_DIR)))

# Try load config from a file (if there is a config file)
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

profile_templates = oneview_client.server_profile_templates

sptfile = open("spts.csv", "r")
with open('spts.csv') as topo_file:
    for line in topo_file:
        fname = line.strip()
        if os.path.isfile(fname):
            with open(fname) as f:
                basic_template_options = json.load(f)
                if profile_templates.get_by_name(basic_template_options["name"]):
                    print("Server Profile Template {} Exists".format(basic_template_options["name"]))
                else:
                    print("Create Server Profile Template {}".format(basic_template_options["name"]))
                    profile_template = profile_templates.create(basic_template_options)
        else:
            print("{} not found".format(fname))
