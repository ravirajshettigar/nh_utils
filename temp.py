import os
import sys
import subprocess

def execWinCommand(command):
    shellResponse = subprocess.check_output(command, stderr=subprocess.STDOUT)
    print(shellResponse.decode('utf-8'))


def readArgumentsFromCommandLine():
    argsMap = {}
    for index in range(1, len(sys.argv)):
        temp = sys.argv[index]
        arg = temp.split("=")
        argsMap[arg[0]] = arg[1]
    return argsMap

