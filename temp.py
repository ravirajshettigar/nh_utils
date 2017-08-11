import os
import sys
import json
import subprocess
import datetime as dt
import xml.etree.ElementTree as xt
import nhutils as nhu

#read existing .json file for pre defined values
with open('pap_5.4.0.json', 'r') as config:
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
                    return True
    return False      



def listRootModules(ROOT_DIR, EXCLUDE_FOLDERS):    
    listAllRootModules = []
    for folder in os.listdir(ROOT_DIR):             
        folder_path = os.path.join(ROOT_DIR, folder)
        pom_xml = folder_path + os.sep + 'pom.xml'        
        if os.path.exists(pom_xml):
            listAllRootModules.append(str(folder_path))
        else:
            listAllRootModules.extend(listRootModules(folder_path, EXCLUDE_FOLDERS))
    return listAllRootModules

def listAllSubModules(listRootModules, EXCLUDE_FOLDERS):
    listSubModules = []
    for rootModule in listRootModules:
        fileList = os.listdir(rootModule)
        subFolderList = []
        pom_xml = os.path.join(rootModule,'pom.xml')
        src_main = os.path.join(rootModule, 'src', 'main')
        if os.path.exists(pom_xml) and os.path.exists(src_main):
                listSubModules.append(rootModule)
        else:
            for aFile in fileList:
                file_path = os.path.join(rootModule, aFile)
                if os.path.isdir(file_path) and not aFile in EXCLUDE_FOLDERS:
                    if not aFile in EXCLUDE_FOLDERS:
                        subFolderList.append(file_path)
            listSubModules.extend(listAllSubModules(subFolderList, EXCLUDE_FOLDERS))
    return listSubModules

if "project_home" in DATA.keys() and "exclude_folders_for_scanning" in DATA.keys():
        ROOT_DIR = DATA["project_home"]        
        EXCLUDE_FOLDERS = DATA["exclude_folders_for_scanning"]
        if "last_run" in DATA.keys() and bool(DATA["last_run"].strip()): 
            last_run = dt.datetime.strptime(DATA["last_run"], '%Y-%m-%d %H:%M:%S.%f')
        else:
            last_run = dt.datetime.now() - dt.timedelta(days=365)

        listRootModules = listRootModules(ROOT_DIR, EXCLUDE_FOLDERS)        
        for subModule in listRootModules:
            print subModule
        print "====================================================="
        print "====================================================="
        listSubModules = listAllSubModules(listRootModules, EXCLUDE_FOLDERS)                
        for subModule in listSubModules:
            print subModule