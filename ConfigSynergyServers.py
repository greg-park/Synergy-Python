# ConfigSynergyServers
#
# This is the main program used to configure Synergy Servers via Python
#

import ReadDataDict

if __name__ == "__main__":

    svrs = []
    print ("Build the dictionary of server info")
    svrs = ReadDataDict.GetServers()

# Just to confirm we have the servers list print out the list of server iLO IP addresses
    print ("Now lets call ListServers")
    ReadDataDict.ListServers(svrs)

# After having the list of servers we need to build Server Profiles
# Data Needed
#   - Server Profile Template
#   - Server iLO IP
#   - Server Profile name (could be generated)
#
#
# Thoughts - create server iLO IP list by quering Synergy
#   - and grabbing all the Server HW.
#   - Note this does not understand if an OS is installed. 
#   -  how to test for os?  
#       Check power state, if OFF boot
#       Once booted need IP (? ... could be random)
#         
# Create Server Profle
#   - Input ServerList[]
#   - Action create profile for each server in list
#   - Verification ... wait till all profiles created
#   - ... check by requesting list of profiles and compare vs. ServerList
#   - Return Success/Failure
#
# Install Operating System
#   - Input ServerList[]
#   - Mount ISO from HTTP server
#   - Boot iso, install OS
#   - Verification ... wait till server booted, ping server
#   - Return Success/Failure