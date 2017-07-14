import os
import datetime as dt

'''stat = os.stat('temp.py')
temp = str(dt.datetime.now())
now = dt.datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
fileTime = dt.datetime.fromtimestamp(stat.st_mtime)
print now
print fileTime
print now < fileTime'''

path = "C:\Development\target\src\target"

if "\target" in path:
    print "Target found"
else:
    print "Target not found"