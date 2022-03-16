# Main Program for Python testing
#
# this program is used to call the functions used to setup
# synergy frames and servers
###

# GJP updates.  Change to "main" that calls as a function
from CheckVersion import version
import MountVirtualMedia 
import ReadDataDict 
import GetApplianceHealthStatus

from pprint import pprint

# Mian
if __name__ == "__main__":
    # check versions     
    # TODO: 
    # Create check the appliance health
    # health_status = appliance_health()
    # pprint(health_status.data)
    
    dc_config = ReadDataDict.DCInfo()
    if dc_config:
        # ConfigEnclosures(dc_config)
        print("Configure Synergy Environment : ",dc_config['enclosure_names'])
        # if CheckEnclosures then ConfigServers
        appliance = GetApplianceHealthStatus.appliance_health(dc_config)
        if appliance:
            print("Success!")
            ver = version()

            # Apply profiles
            # Verify profiles
            # Install OS
            #
            svrs = []
            print ("Build the dictionary of server info")
            svrs = ReadDataDict.GetServers(dc_config)
            ReadDataDict.ListServers(svrs)
            print ("Make sure no ISO media is already mouted")
            MountVirtualMedia.UnMountServerISO(svrs)
            #print ("Mount OS ISO as descried in data.csv")
            #MountVirtualMedia.MountServerISO(svrs)
            # Verify OS installation
        else:
            print("MAJOR MELTDOWN FAILURE")    