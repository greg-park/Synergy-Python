# Main Program for Python testing
#
# this program is used to call the functions used to setup
# synergy frames and servers
###
# Just a place to test python examples

from datetime import datetime
import time

def GetTimeStamp():
#    timestamp = 1625309472.357246
    timestamp = time.time()
    # convert to datetime
    date_time = datetime.fromtimestamp(timestamp)

    # convert timestamp to string in dd-mm-yyyy HH:MM:SS
    str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
    print("[{}]".format(str_date_time))

GetTimeStamp()
time.sleep(10)
GetTimeStamp()