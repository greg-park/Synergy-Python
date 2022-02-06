# Main Program for Python testing
#
# this program is used to call the functions used to setup
# synergy frames and servers
###

# GJP updates.  Change to "main" that calls as a function
from GetApplianceHealtyStatus import appliance_health
from CheckVersion import version
import MountVirtualMedia 
import ReadDataDict 

from pprint import pprint

# Mian
if __name__ == "__main__":
    # check versions
    ver = version()
    pprint(ver)
    for key,value in ver.items():
        print(key, ':', value)
        
    # check the appliance health
    health_status = appliance_health()
    # pprint(health_status.data)
    svrs = []
    print ("Build the dictionary of server info")
    svrs = ReadDataDict.GetServers()
    print ("Make sure no ISO media is already mouted")
    MountVirtualMedia.UnMountServerISO(svrs)
    print ("Mount OS ISO as descried in data.csv")
    MountVirtualMedia.MountServerISO(svrs)