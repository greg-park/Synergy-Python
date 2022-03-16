# Notepad ...
# TODO:
# Get server install info
# Use iLO IP to create Server Profile
# after Profile is created Install OS

from ConfigLoader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient
import json
import platform    # For getting the operating system name
import subprocess  # For executing a shell command

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>",
    },
    "api_version": "<api_version>"
}

# Use this function to ping and test IPs
def ping(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    result = subprocess.Popen(command,stdout=subprocess.PIPE)
    stdout, stderr = result.communicate()
    return (result.returncode)
    
if ping("10.10.108.1") == 0:
    print("Server is up")
else:
    print("Server not found")

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
jsonfiles = config['json_dir']

# Build a list of the IPs for the iLOs.  This list will be used to
# 1. Apply profiles
# 2. Mount ISO and install operating systems
print("Get list of all the servers iLO IPs from appliance: ")
servers = oneview_client.server_hardware.get_all()

# With each of the iLOs run through the list and:
# 1. Create the target json files to hold info for installations
# 2. Check for Profiles
for svr in servers:
#   Create unique json file for installation.
    installJson = jsonfiles+(svr['mpHostInfo']['mpHostName']).split('.')[0]+".json"

#   File contains:
#       - Defined data in config.json
#           - Server Profile Template from config.json
#           - Server OS, iso and http location of iso
#       - iLO IP and iLO hostname
#       - server hostname(read from config.json)+increment
#       - server host IP.  Same network ID on different network
    temp_ip = ""
    with open(file=installJson, mode="w") as output_file:
        srv_number = svr['mpHostInfo']['mpIpAddresses'][2]['address'].split('.')[3]
        temp_ip = config['install_info']['hostnet']+"."+srv_number
        temp_hostname = config['install_info']['basename']+"_"+srv_number
        print(temp_ip)
        config['install_info']['hostname'] = temp_hostname
        config['install_info']['hostIP'] = temp_ip
        config['install_info']['iloIP'] = svr['mpHostInfo']['mpIpAddresses'][2]['address']
        json.dump(config['install_info'], output_file, indent=5)
#        json.dump(svr['mpHostInfo'], output_file, indent=5)

# ping iLO IP
# check_host_profile
# check_host_power
# boot_ISO_Media/Install
### __main__
#if __name__ == "__main__":
#    HostiLOInfo()