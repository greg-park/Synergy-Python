##############################################################################
# UpdateCompliance.py
# - Script for compliance of profiles vs SPT.
#
#   VERSION 1.0
#   Date:
#   Input: config.json
#   Output: Status during execution
#
#   Changes:
#
#   Notes:
#
############################################################################## 

from pprint import pprint
from ConfigLoader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

#from itertools import ifilter

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>",
    },
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)

print("Get list of all the servers profiles from appliance: ")
server_profiles = oneview_client.server_profiles

for profile in server_profiles.get_all(sort='name:ascending'):
    profile_compliance = server_profiles.get_by_name(profile['name'])
    print("Check server compliance: {}".format(profile['name']))
    schema = profile_compliance.get_compliance_preview()
    if profile['templateCompliance'] == "NonCompliant":
        pprint("Set complaince for {}".format(profile['name']))
        profile_compliance.patch(operation="replace",path="/templateCompliance", value="Compliant")