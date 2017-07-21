import os
import sys
import json
import datetime as dt
import nhutils as nhu
import secutils as sec

buildScripts = []
deployScripts = []
executionTime = dt.datetime.now()
completeBuildRequired = False
cleanRequired = False
appCode = "pap"
bugId = 9999
completeBuild = 'n'
cleanRequired = 'n'

'''appCode=raw_input("Enter the application code >> ").strip()
if not os.path.exists(appCode + '.json'):
    print("You have entered invalid app code [hint: app code is filname of <<app>>.json which contains configuration]")
    sys.exit()

bugId=raw_input("Enter bug id >> ").strip()

completeBuild=raw_input("Do you want to perform complete build? [y/n] >> ").strip().lower()
if completeBuild == "y":
    completeBuildRequired = True

cleanBuild = raw_input("Do you want to perform clean build? [y/n] >> ").strip().lower()
if cleanBuild == "y": cleanRequired = True'''

#read existing .json file for pre defined values
with open(appCode + '.json', 'r') as config:
    DATA = json.load(config)

build_script_file = "build.bat"
deploy_script_file = "deploy.bat"
useRobocopy = False
if "bug" in DATA.keys(): 
    build_script_file = "build_" + bugId + ".bat"
    deploy_script_file = "deploy_" + bugId + ".bat"
if "enable_robocopy" in DATA.keys():
    useRobocopy = DATA["enable_robocopy"]

credentials = sec.processAuthenticationInfo(DATA) #save credentials to cache or read authentication info from cache
#nhu.startFiddler(DATA) #start fiddler
#nhu.startShrewsoftVPN(DATA, credentials) #start vpn connection


if cleanRequired:
    print 'test'
else:
    listRecentlyModifiedModules, listOfGwtModules, listAllModules = nhu.listRecentlyModifiedModules(DATA) #identify list of recently modified modules and gwt modules
    buildScripts.extend(nhu.getEnvironmentVariableScript(DATA)) #set all environment variable
    buildScripts.extend(nhu.getMvnInstallCommandScript(listRecentlyModifiedModules, cleanRequired, DATA)) #execute maven command for modified maven projects
    nhu.writeLineInListToFile(buildScripts, build_script_file)

    #nhu.execWinCommand(build_script_file, "Build Log [" + bugId + "] : " + executionTime)
    #PART 1 - ends here, which performs the intelligent build for modified projects only
    readyToDeployJarFileMap = nhu.listJarFilesFromTargetFolders(listRecentlyModifiedModules)
    tomcatLibDeployScripts = nhu.getTomcatAppDeployScripts(DATA, readyToDeployJarFileMap, listAllModules)
    deployScripts.extend(tomcatLibDeployScripts)
    hsipProductDeployScript = nhu.getHsipProductDeployScripts(DATA, readyToDeployJarFileMap, listAllModules)
    deployScripts.extend(hsipProductDeployScript)
    #sourceWebFolderList = nhu.listWebFoldersFromTargetFolders(listRecentlyModifiedModules)
    #targetFolder = "C:\\Users\\Raviraj\\Downloads"
    #deployScripts.extend(nhu.getCopyPasteFoldersScript(sourceWebFolderList, targetFolder, useRobocopy))

startServicemixScript = nhu.startServiceMix(DATA, cleanRequired)
deployScripts.extend(startServicemixScript)
startTomcatScript = nhu.startTomcatScript(DATA)
deployScripts.extend(startTomcatScript)

nhu.writeLineInListToFile(deployScripts, deploy_script_file)
#nhu.execWinCommand(deploy_script_file, "Deploy Log [" + bugId + "] : " + executionTime)

#PART 2 - ends here, which performs deployment of build files

#updating the last run variables and resaving it to .json file for next run usage
DATA['last_run'] = str(dt.datetime.now())
with open(appCode + '.json', 'w') as config:
    json.dump(DATA, config, indent=4)
