#
# Adapted from HPE Python Scripts
# Use this to check the OneView library is at the proper version
###

from pprint import pprint
from hpeOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

def version():
    config = {
        "ip": "<oneview_ip>",
        "credentials": {
            "userName": "<username>",
            "password": "<password>"
        }
    }

    # Try load config from a file (if there is a config file)
    config = try_load_from_file(config)

    oneview_client = OneViewClient(config)

    # Get the current version and the minimum version
    print("Get the current version and the minimum version")
    return (oneview_client.versions.get_version())
#    pprint(version['currentVersion'])
#    pprint(version)

ver = version()
pprint(ver['currentVersion'])