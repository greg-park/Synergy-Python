##############################################################################
# ImportSPT.py
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
from fileinput import filename
from ConfigLoader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient
import json, os.path

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
# print(os.path.isdir(JSON_DIR))

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
try:
    oneview_client = OneViewClient(config)
except Exception as e:
    print('Connect Error:', e)
    exit()

print("Import Server Profile Templates from json files")
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
