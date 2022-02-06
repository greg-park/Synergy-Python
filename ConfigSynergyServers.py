import ReadDataDict

if __name__ == "__main__":
    svrs = []
    print ("Build the dictionary of server info")
    svrs = ReadDataDict.GetServers()
    print ("Now lets call ListServers")
    ReadDataDict.ListServers(svrs)