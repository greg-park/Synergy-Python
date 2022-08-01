from pprint import pprint

# import the hpeOneView library
# pip install hpeOneView
# pip install tabulate
from tabulate import tabulate
from hpeOneView.oneview_client import OneViewClient
from ConfigLoader import try_load_from_file

# Edit this info in config.json for your instance
config = {
    "api_version": 3400,
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>",
    }
}
config = try_load_from_file(config)

# connect to the hpeOneView instance

try:
    oneview_client = OneViewClient(config)
except Exception as e:
    print('Connect Error:', e)
    exit()

server_profiles = oneview_client.server_profiles.get_all()
servers = oneview_client.server_hardware

profiles = []
noProfiles = []

for profile in server_profiles:
    # pprint(profile)
    #print(profile['name'])
    #print(profile['uri'])    
    #print(profile['macType'])
    macs = []
    for connection in profile['connectionSettings']['connections']:        
        if connection['functionType'] == 'Ethernet':
            #print("Name : " + connection['name'])
            #print("mac: " + connection['mac'])
        #    if connection['name'] == "Mgmt1":
            macDict = {'nic': connection['name'], 'enclosureBay': profile['enclosureBay'],'macAddress': connection['mac']}
            profiles.append(macDict)

    pDict = {'name': profile['name'], 'macType': profile['macType'], 'macs': macs}
#    profiles.append(pDict)

print(tabulate(profiles, headers='keys', tablefmt='orgtbl'))
#for profile in profiles:
#    pprint(profile)
    #for macaddress in profile['macs']:
    #    print("{},{},{}".format(profile['name'], str(profile['enclosureBay']), macaddress['macAddress']))

for np in noProfiles:
    pprint(profile)