# Code to build a dictionary out of a CSV file
# this dictionary is focused on automted installaiton of 
# Synergy blades in a OneView environment
#
# data.cs structure
# iloIP,User,Pass,isoDir,iso,ksTemplate,NewCfg,NewIP,NewHostName,ESXUser,ESXpwd
#
# Notepad ...
# Structure of data needs to ahve
# * Individuall for each server
#   * IP
#   * iLO IP
#   * Hostname
#   * iLO Hostname
#   * dir for kickstart
# * stays the same
#   * ISO location, ISO
#   * Kickstrat file name 
#   * Domain
#
# - could create uniqne names for ks based off IP/Hostname.  Reduces data.csv 
# - could create a file for the non changing data and one for change data
#

import csv

def GetServers():
    servers = []
    count = 0
    # opening the CSV file
    with open('data.csv', mode ='r') as file:   

           # reading the CSV file
           csvFile = csv.DictReader(file)
    
           # displaying the contents of the CSV file
           for lines in csvFile:
               servers.append(lines)
               # print(servers[count]['iloIP'])
               count = count + 1
    return servers

def ListServers(svrList = [], *args):
    for s in svrList:
        print(s['iloIP'])

if __name__ == "__main__":
    svrs = []
    print ("I'm Here!")
    svrs = GetServers()
#    print ("Now lets call ListServers")
    ListServers(svrs)