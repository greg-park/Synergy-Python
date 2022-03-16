# Functions used for program
#
# code adapted from https://stackoverflow.com/questions/37140846/how-to-convert-ipv6-link-local-address-to-mac-address-in-python
# for the conversion process check https://nettools.club/mac2ipv6 
#
# mac2ipv6 - convert a HW MAC Id to a IPv6 address 
# based on standards
# input = macID in AA:BB:CC:DD:EE:FF format
# return = IPv6 address as link local (fe80) address

def mac2ipv6(mac):
    # only accept MACs separated by a colon
    parts = mac.split(":")

    # modify parts to match IPv6 value
    parts.insert(3, "ff")
    parts.insert(4, "fe")
    parts[0] = "%x" % (int(parts[0], 16) ^ 2)

    # format output
    ipv6Parts = []
    for i in range(0, len(parts), 2):
        ipv6Parts.append("".join(parts[i:i+2]))
    ipv6 = "fe80::%s/64" % (":".join(ipv6Parts))
    return ipv6

# ipv62mac - convert a IPv6 address to HW MAC Id
# based on standards
# input = ipv6 address as A:B:C:D:E:F:G:H format
# return = MAC Id as AA:BB:CC:DD:EE:FF format
def ipv62mac(ipv6):
    # remove subnet info if given
    subnetIndex = ipv6.find("/")
    if subnetIndex != -1:
        ipv6 = ipv6[:subnetIndex]

    ipv6Parts = ipv6.split(":")
    macParts = []
    for ipv6Part in ipv6Parts[-4:]:
        while len(ipv6Part) < 4:
            ipv6Part = "0" + ipv6Part
        macParts.append(ipv6Part[:2])
        macParts.append(ipv6Part[-2:])

    # modify parts to match MAC value
    macParts[0] = "%02x" % (int(macParts[0], 16) ^ 2)
    del macParts[4]
    del macParts[3]

    return ":".join(macParts)

# Main for testing
#ipv6 = mac2ipv6("94:40:C9:32:98:AA")
#back2mac = ipv62mac(ipv6)
#print ("IPv6:", ipv6)
#print ("MAC:", back2mac)