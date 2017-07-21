import os
import sys
import json
import subprocess

import nhutils as nhu

#read existing .json file for pre defined values
with open('pap.json', 'r') as config:
    DATA = json.load(config)

def printList(anyList):
    for text in anyList:
        print text
    return

def execWinCommand(command):
    shellResponse = subprocess.check_output(command, stderr=subprocess.STDOUT)
    print(shellResponse.decode('utf-8'))
    return

def readArgumentsFromCommandLine():
    argsMap = {}
    for index in range(1, len(sys.argv)):
        temp = sys.argv[index]
        arg = temp.split("=")
        argsMap[arg[0]] = arg[1]
    return argsMap
def killAllOpenCMDs():
    return ['taskkill /f /im cmd.exe']

def getTomcatProjectSpecificJars(projectName):
    jarList = []
    tomcatProjectLibPath = "C:\\Development\\servers\\apache_tomcat_pap" + os.sep + "webapps" + os.sep + projectName + os.sep + "WEB-INF" + os.sep + "lib"
    for jarFile in os.listdir(tomcatProjectLibPath):
        print(jarFile)
        jarList.append(jarFile)
    return jarList

#getTomcatProjectSpecificJars("patientApp")
#getTomcatProjectSpecificJars("providerApp")



printList(killAllOpenCMDs())
tomcatScript = startTomcatScript(DATA)
printList(tomcatScript)
servicemixScript = startServiceMix(DATA, False)
printList(servicemixScript)

subprocess.Popen('taskkill /F /IM cmd.exe')
subprocess.Popen('taskkill /F /IM cmd.exe')