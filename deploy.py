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
bugId = None
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
if not bugId == None and len(bugId.strip()) > 0: 
    build_script_file = "build_" + bugId + ".bat"
    deploy_script_file = "deploy_" + bugId + ".bat"
if "enable_robocopy" in DATA.keys():
    useRobocopy = DATA["enable_robocopy"]

credentials = sec.processAuthenticationInfo(DATA) #save credentials to cache or read authentication info from cache
#nhu.startFiddler(DATA) #start fiddler
#nhu.startShrewsoftVPN(DATA, credentials) #start vpn connection

completeBuildRequired = completeBuild.strip().lower()[0:1] == 'y'

buildScripts.extend(nhu.getEnvironmentVariableScript(DATA)) #set all environment variable

listAllRootModules = nhu.listRootModules(DATA)
buildScripts.extend(nhu.performSvnUpdate(listAllRootModules))

if completeBuildRequired:    
    buildScripts.extend(nhu.getMvnInstallCommandScript(listAllRootModules, cleanRequired, DATA)) #execute maven command for modified maven projects
else:
    listRecentlyModifiedModules, listOfGwtModules, listAllModules = nhu.listRecentlyModifiedModules(DATA) #identify list of recently modified modules and gwt modules
    buildScripts.extend(nhu.getMvnInstallCommandScript(listRecentlyModifiedModules, cleanRequired, DATA)) #execute maven command for modified maven projects

nhu.writeLineInListToFile(buildScripts, build_script_file)
#nhu.execWinCommand(build_script_file, "Build Log [" + bugId + "] : " + executionTime)

if completeBuildRequired:
    tomcatWarDeployScripts = nhu.getTomcatWARDeployScripts(DATA)
    deployScripts.extend(tomcatWarDeployScripts)
    hsipProductDeployScript = nhu.getHsipProductDeployScripts(DATA)
    deployScripts.extend(hsipProductDeployScript)
    if cleanRequired:
        nhu.cleanServiceMixCacheScript(DATA)
else:
    readyToDeployJarFileMap = nhu.listJarFilesFromTargetFolders(listRecentlyModifiedModules)
    tomcatLibDeployScripts = nhu.getTomcatAppDeployScripts(DATA, readyToDeployJarFileMap, listAllModules)
    deployScripts.extend(tomcatLibDeployScripts)
    hsipProductDeployScript = nhu.getHsipProductDeployScripts(DATA, readyToDeployJarFileMap, listAllModules)
    deployScripts.extend(hsipProductDeployScript)
#sourceWebFolderList = nhu.listWebFoldersFromTargetFolders(listRecentlyModifiedModules)
#targetFolder = "C:\\Users\\Raviraj\\Downloads"
#deployScripts.extend(nhu.getCopyPasteFoldersScript(sourceWebFolderList, targetFolder, useRobocopy))

startServicemixScript = nhu.startServiceMixScript(DATA)
deployScripts.extend(startServicemixScript)
startTomcatScript = nhu.startTomcatScript(DATA)
deployScripts.extend(startTomcatScript)

nhu.writeLineInListToFile(deployScripts, deploy_script_file)
#nhu.execWinCommand(deploy_script_file, "Deploy Log [" + bugId + "] : " + executionTime)

#updating the last run variables and resaving it to .json file for next run usage
DATA['last_run'] = str(dt.datetime.now())
with open(appCode + '.json', 'w') as config:
    json.dump(DATA, config, indent=4)
