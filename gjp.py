# Main Program for Python testing
#
# this program is used to call the functions used to setup
# synergy frames and servers
###

# GJP updates.  Change to "main" that calls as a function
from appliance_health_status import appliance_health
from versions import version
from pprint import pprint

# check versions
version()
# check the appliance health
health_status = appliance_health()
pprint(health_status.data)