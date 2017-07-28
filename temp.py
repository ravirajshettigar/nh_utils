import os
import sys
import json
import subprocess
import datetime as dt
import xml.etree.ElementTree as xt
import nhutils as nhu

#read existing .json file for pre defined values
with open('prp_5.4.0.json', 'r') as config:
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

def checkForFileCreationAndModifications(pathToFolder, last_run):
    for root, subFolders, files in os.walk(pathToFolder):
        for anyFile in files:
            filePath = os.path.join(root, anyFile)            
            if os.path.isfile(filePath):
                fileStat = os.stat(filePath)                    
                modifiedTime = dt.datetime.fromtimestamp(fileStat.st_mtime)
                createdTime = dt.datetime.fromtimestamp(fileStat.st_ctime)                    
                if last_run < createdTime or last_run < modifiedTime:
                    print filePath + " was modified"
    return           


#checkForFileCreationAndModifications("C:\\PrP\\v5.4.0\\AppManager\\src")


def listRecentlyModifiedModules(ROOT_DIR, EXCLUDE_FOLDERS, LAST_RUN):
    listOfModifiedModules = []
    is_gwt_project =False
    pom_xml = os.path.join(ROOT_DIR, 'pom.xml')
    src_folder = os.path.join(ROOT_DIR,'src','main')
    if os.path.exists(pom_xml) and os.path.exists(src_folder):
        checkForFileCreationAndModifications(os.path.join(ROOT_DIR, 'src'), LAST_RUN)
    else:
        for obj in os.listdir(ROOT_DIR):
            path = os.path.join(ROOT_DIR, obj)
            if os.path.isdir(path):
                listRecentlyModifiedModules(path, EXCLUDE_FOLDERS, LAST_RUN)
    return listOfModifiedModules

if "project_home" in DATA.keys() and "exclude_folders_for_scanning" in DATA.keys():
        ROOT_DIR = DATA["project_home"]        
        EXCLUDE_FOLDERS = DATA["exclude_folders_for_scanning"]
        if "last_run" in DATA.keys() and bool(DATA["last_run"].strip()): 
            last_run = dt.datetime.strptime(DATA["last_run"], '%Y-%m-%d %H:%M:%S.%f')
        else:
            last_run = dt.datetime.now() - dt.timedelta(days=365)
        listRecentlyModifiedModules(ROOT_DIR, EXCLUDE_FOLDERS, last_run)
