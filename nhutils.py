import os
import sys
import subprocess
import datetime as dt
import xml.etree.ElementTree as xt

def execWinCommand(command, titleForLog):
    shellResponse = subprocess.check_output(command, stderr=subprocess.STDOUT)
    log(titleForLog, shellResponse.decode('utf-8'))
    return

def readArgumentsFromCommandLine():
    argsMap = {}
    for index in range(1, len(sys.argv)):
        temp = sys.argv[index]
        arg = temp.split("=")
        argsMap[arg[0]] = arg[1]
    return argsMap

def log(title, data):
    with open('deploy_log.txt', 'a') as newFile:
        newFile.write("=========================" + dt.datetime.now() + "=========================")
        newFile.write("=========================" + title + "=========================")
        newFile.write(data)
        newFile.write("=========================" + title + "=========================")
    return
def writeLineInListToFile(linesInList, fileNameWithExtension):
    with open(fileNameWithExtension, 'w') as newFile:
        for line in linesInList:
            newFile.write(line)
            newFile.write('\n')
    return

def startFiddler(config):
    if "enable_fiddler" in config.keys():
        if "fiddler_executable" in config.keys() and len(config["fiddler_executable"].strip()) > 0:
            subprocess.Popen(config["fiddler_executable"])
    return

def startShrewsoftVPN(config, credentials):
    if "enable_vpn" in config.keys():
        if "vpn_executable" in config.keys() and len(config["vpn_executable"].strip()) > 0:
            subprocess.Popen(config["vpn_executable"] + " -u " + credentials[0] + " -p " + credentials[1] + " -a")
    return

def listJarFilesFromTargetFolders(moduleFolderList):
    jarFilesMap = {}
    for folderPath in moduleFolderList:
        targetFolder = folderPath + os.sep + "target"
        if os.path.exists(targetFolder):
            fileList = os.listdir(targetFolder)
            for fileName in fileList:
                if fileName.endswith(".jar"):
                    jarFilesMap[fileName] = targetFolder + os.sep + fileName
    return jarFilesMap

def listWebFoldersFromTargetFolders(moduleFolderList):
    listWebFolders = []
    for folderPath in moduleFolderList:
        targetFolder = folderPath + os.sep + "target"
        if os.path.exists(targetFolder):
            for root, subFolders, files in os.walk(targetFolder):
                for folder in subFolders:
                    folder_path = root + os.sep + folder
                    web_folder_path = folder_path + os.sep + "WEB-INF" + os.sep + "classes"
                    if os.path.exists(web_folder_path):
                        listWebFolders.append(folder_path)
                        break
                break
    return listWebFolders

def listRootModules(config):
    listAllRootModules = []
    if "project_home" in config.keys():
        ROOT_DIR = config["project_home"]
        for root, subFolders, files in os.walk(ROOT_DIR):
            for folder in subFolders:               
                folder_path = root + os.sep + folder
                pom_xml = folder_path + os.sep + 'pom.xml'
                src_folder = folder_path + os.sep + 'src' + os.sep + 'main'
                if os.path.exists(pom_xml) and not os.path.exists(src_folder):
                    listAllRootModules.append(str(folder_path))
                    break 
    return listAllRootModules

def listRecentlyModifiedModules(config):
    listOfModifiedModules = []
    listOfGwtModules = []
    listAllModules = []

    if "project_home" in config.keys() and "exclude_folders_for_scanning" in config.keys():
        ROOT_DIR = config["project_home"]
        
        EXCLUDE_FOLDERS = config["exclude_folders_for_scanning"]

        if "last_run" in config.keys() and bool(config["last_run"].strip()): 
            last_run = dt.datetime.strptime(config["last_run"], '%Y-%m-%d %H:%M:%S.%f')
        else:
            last_run = dt.datetime.now() - dt.timedelta(days=365)
            
        for root, subFolders, files in os.walk(ROOT_DIR):            
            for exFolder in EXCLUDE_FOLDERS:
                if exFolder in subFolders:
                    subFolders.remove(exFolder)

            for folder in subFolders:               
                folder_path = root + os.sep + folder            
                is_gwt_project =False
                pom_xml = folder_path + os.sep + 'pom.xml'
                src_folder = folder_path + os.sep + 'src' + os.sep + 'main'
                if os.path.exists(pom_xml) and os.path.exists(src_folder):
                    listAllModules.append(str(folder_path))
                    for s_root, s_subFolders, s_files in os.walk(folder_path):                        
                        for exFolder in EXCLUDE_FOLDERS:
                            if exFolder in s_subFolders:
                                s_subFolders.remove(exFolder)

                        for s_folder in s_subFolders:                        
                            if not folder_path in listOfGwtModules:
                                for s_file in s_files:
                                    if s_file.endswith(".gwt.xml"):
                                        listOfGwtModules.append(str(folder_path))
                                        break
                            if not folder_path in listOfModifiedModules:     
                                for s_file in s_files:
                                    file_path = s_root + os.sep + s_file
                                    file_stat = os.stat(file_path)
                                    mtime = dt.datetime.fromtimestamp(file_stat.st_mtime)  
                                    ctime = dt.datetime.fromtimestamp(file_stat.st_ctime)                            
                                    if last_run < mtime or last_run < ctime:
                                        listOfModifiedModules.append(str(folder_path))
                                        break
                            continue               
    return listOfModifiedModules, listOfGwtModules, listAllModules

def getEnvironmentVariableScript(config): 
    scriptSteps = []
    if "extended_path_variable" in config.keys():        
        if len(config["extended_path_variable"].strip()) > 0:
            scriptSteps.append("set \"path=" + os.environ["path"] + ';' + config["extended_path_variable"] + "\"")

    if "environment_variables" in config.keys():
        envSetList = config["environment_variables"]
        for envSet in envSetList:
            scriptSteps.append("set \"" + envSet + "\"")
    
    if "enable_fiddler" in config.keys() and "extended_fiddler_config" in config.keys():
        scriptSteps.append("set \"catalina_opts=%catalina_opts% " + config["extended_fiddler_config"] + "\"")
        scriptSteps.append("set \"karaf_opts=%karaf_opts% " + config["extended_fiddler_config"] + "\"")
    
    if "enable_debug" in config.keys():
        if "extended_catalina_debug_config" in config.keys():
            scriptSteps.append("set \"catalina_opts=%catalina_opts% " + config["extended_catalina_debug_config"] + "\"")
        if "extended_karaf_debug_config" in config.keys():
            scriptSteps.append("set \"karaf_opts=%karaf_opts% " + config["extended_karaf_debug_config"] + "\"")
    
    return scriptSteps

def getCopyPasteFilesScript(sourceFilePathList, targetFolder):
    scripts = [] 
    if os.path.exists(targetFolder):
        for filePath in sourceFilePathList:
            scripts.append("copy /y " + filePath + " " + targetFolder)
    return scripts
        
def getCopyPasteFoldersScript(sourceFolderPathList, targetFolder, useRobocopy):
    scripts = []
    if os.path.exists(targetFolder):
        if useRobocopy:
            for sourceFolderPath in sourceFolderPathList:
                scripts.append("robocopy " + sourceFolderPath + " " + targetFolder + " /copy:DAT")
        else:
            for sourceFolderPath in sourceFolderPathList:
                scripts.append("xcopy " + sourceFolderPath + " " + targetFolder + " /e /q /y")
    return scripts

def getMvnInstallCommandScript(mavenProjectFolderList, cleanRequired, config):
    scripts = []
    clean = ""
    extended_maven_attributes = ""
    if cleanRequired: clean = "clean "
    if "extended_maven_attributes" in config.keys(): extended_maven_attributes = config["extended_maven_attributes"]
    for mvnProject in mavenProjectFolderList:
        scripts.append("mvn " + clean + "install " + mvnProject + " -am " + extended_maven_attributes)
    return scripts

def getEnvVariableValueFromConfig(envVar, config):
    value = None
    if "environment_variables" in config.keys():
        for envConfig in config["environment_variables"]:
            parts = envConfig.split("=")
            if parts[0] == envVar:
                value = parts[1]
                break
    return value

def getServiceMixBundleMappings(config):
    bundles = {}
    hsipHome = getEnvVariableValueFromConfig("servicemix_home", config)
    serviceMixCachePath = os.path.join(hsipHome, "data", "cache")
    for folder in os.listdir(serviceMixCachePath):
        bundleLocationFile = serviceMixCachePath + os.sep + folder + os.sep + "bundle.location"        
        if os.path.exists(bundleLocationFile):
            with open(bundleLocationFile, "r") as location:
                content = location.readline()
                if content.strip().startswith('file:'):
                    clen = len(content)
                    lidx = content[::-1].find("/")
                    fileName = content[clen - lidx:]
                    bundles[fileName] = folder
    return bundles

def performSvnUpdate(listAllRootModules):
    scripts = []
    for rootModule in listAllRootModules:
        scripts.append("cd /d \"" + str(rootModule) + "\"")
        scripts.append("svn update")
    return scripts

def deleteExistingWARAndAppFolder(tomcatHome, appName):
    return [
        "del /f /s /q \"" + os.path.join(tomcatHome, "webapps", appName + ".war") +"\"",
        "rmdir /s /q \"" + os.path.join(tomcatHome, "webapps", appName) +"\""
    ]


def getTomcatWARDeployScripts(config):
    tomcatWARDeployScript = []
    tomcatHome = getEnvVariableValueFromConfig("catalina_home", config)
    if "tomcat_deploy_config" in config.keys():
        for sourceConfig in config["tomcat_deploy_config"]:
            for module in listAllModules: 
                deployList = []
                if module.strip().endswith(os.path.join(sourceConfig["project"], sourceConfig["module"])):
                    warFile = os.path.join(module, "target", sourceConfig["target"] + ".war")
                    deployList.append(warFile)
                    tomcatAppDeployScript.extend(deleteExistingWARAndAppFolder(tomcatHome, sourceConfig["target"]))
                    tomcatAppDeployScript.extend(getCopyPasteFilesScript(deployList, os.path.join(tomcatHome,"webapps")))
                break
    return tomcatAppDeployScript

def getTomcatAppDeployScripts(config, readyToDeployJarFileMap, listAllModules):
    tomcatAppDeployScript = []
    tomcatHome = getEnvVariableValueFromConfig("catalina_home", config)
    if "tomcat_deploy_config" in config.keys():
        for sourceConfig in config["tomcat_deploy_config"]:
            for module in listAllModules:                
                if module.strip().endswith(os.path.join(sourceConfig["project"], sourceConfig["module"])):
                    pomComponentList = parsePomXML(os.path.join(module, "pom.xml"))
                    deployList = []
                    for jarFile, jarPath in readyToDeployJarFileMap.items():
                        if jarFile in pomComponentList:                            
                            deployList.append(jarPath)                    
                    tomcatAppDeployScript.extend(getCopyPasteFilesScript(deployList, os.path.join(tomcatHome,"webapps", sourceConfig["target"], "WEB-INF", "lib")))
                break
    return tomcatAppDeployScript

def parsePomXML(pomFilePath):
    ns = {'maven': 'http://maven.apache.org/POM/4.0.0'}
    pomComponentList = []
    versionMappings = {}
    tree = xt.parse(pomFilePath)
    root = tree.getroot()  
    versionMappings['${project.version}'] = root.find('maven:parent', ns).find('maven:version', ns).text    
    propertiesElement = root.find('maven:properties', ns)
    for child in propertiesElement:        
        tagName = child.tag.replace('{' + ns['maven'] + '}', '')
        versionMappings['${' + tagName + '}'] = child.text

    dependencies = root.find('maven:dependencies', ns).findall('maven:dependency', ns)    
    for dependency in dependencies:
        versionElement = dependency.find('maven:version', ns)
        if xt.iselement(versionElement):
            if versionElement.text in versionMappings.keys():
                component = dependency.find('maven:artifactId', ns).text
                version = versionMappings[versionElement.text]  
                pomComponentList.append(component + "-" + version + ".jar")                
    return pomComponentList

def getHsipProductDeployScripts(config):
    hsipProductDeployScript = []
    hsipHome = getEnvVariableValueFromConfig("servicemix_home", config)
    if "bundle_deploy_config" in config.keys():        
        for sourceConfig in config["bundle_deploy_config"]:
             for module in listAllModules:                
                if module.strip().endswith(os.path.join(sourceConfig["project"], sourceConfig["module"])):
                    hsipInTargetFolder = identifyHsipDeploySource(module)
                    featureXml = None
                    deployFiles = os.listdir(os.path.join(hsipInTargetFolder, "deploy"))
                    if len(deployFiles) > 1:
                        for fileName in deployFiles:
                            if "name_contains" in sourceConfig.keys():
                                if fileName.find(sourceConfig["name_contains"]) > -1 and fileName.endswith('.xml'):
                                    featureXml = fileName
                                    break
                            elif fileName.endswith(".xml"):                                
                                    featureXml = fileName
                                    break                    
                    if featureXml == None:
                        print("Failed to locate the feature xml file in " + hsipInTargetFolder + ", System will exit")
                        continue
                    hsipProductDeployScript.extend(getCopyPasteFilesScript([os.path.join(os.path.join(hsipInTargetFolder, "deploy"), featureXml)], os.path.join(hsipHome,"deploy")))
                    deployList = []
                    productFolder = os.path.join(hsipInTargetFolder, "Carefx", "Products", sourceConfig["target"])
                    for jarFile in os.listdir(productFolder):
                        deployList.append(os.path.join(productFolder, jarFile))                    
                    hsipProductDeployScript.extend(getCopyPasteFilesScript(deployList, os.path.join(hsipHome,"Carefx", "Products", sourceConfig["target"])))
                break
    return hsipProductDeployScript

def getHsipProductDeployScripts(config, readyToDeployJarFileMap, listAllModules):
    hsipProductDeployScript = []
    hsipHome = getEnvVariableValueFromConfig("servicemix_home", config)
    bundleMappings = getServiceMixBundleMappings(config)
    if "bundle_deploy_config" in config.keys():        
        for sourceConfig in config["bundle_deploy_config"]:
             for module in listAllModules:                
                if module.strip().endswith(os.path.join(sourceConfig["project"], sourceConfig["module"])):                    
                    hsipInTargetFolder = identifyHsipDeploySource(module)
                    featureXml = None
                    deployFiles = os.listdir(os.path.join(hsipInTargetFolder, "deploy"))
                    if len(deployFiles) > 1:
                        for fileName in deployFiles:
                            if "name_contains" in sourceConfig.keys():
                                if fileName.find(sourceConfig["name_contains"]) > -1 and fileName.endswith('.xml'):
                                    featureXml = fileName
                                    break
                            elif fileName.endswith(".xml"):                                
                                    featureXml = fileName
                                    break                    
                    if featureXml == None:
                        print("Failed to locate the feature xml file in " + hsipInTargetFolder + ", System will exit")
                        continue

                    featureComponentList = parseFeaturesXML(os.path.join(hsipInTargetFolder, "deploy", featureXml))
                    deployList = []
                    deleteList = []
                    for jarFile, jarPath in readyToDeployJarFileMap.items():
                        if jarFile in featureComponentList:
                            deployList.append(jarPath) 
                            deleteList.append(jarFile)                   
                    hsipProductDeployScript.extend(getCopyPasteFilesScript(deployList, os.path.join(hsipHome,"Carefx", "Products", sourceConfig["target"])))
                    hsipProductDeployScript.extend(deleteBundleCacheForJar(hsipHome, deleteList, bundleMappings))
    return hsipProductDeployScript

def deleteBundleCacheForJar(hsipHome, deleteList, bundleMappings):    
    deleteScripts = []
    cacheLocation = os.path.join(hsipHome, "data", "cache")
    for jarFile in deleteList:
        if jarFile in bundleMappings.keys():
            deleteScripts.append('rmdir /s /q ' + os.path.join(cacheLocation, str(bundleMappings[jarFile])))
    return deleteScripts

def parseFeaturesXML(featuresFilePath):
    ns = {'karaf': 'http://karaf.apache.org/xmlns/features/v1.0.0'}
    featureComponentList = []
    versionMappings = {}
    tree = xt.parse(featuresFilePath)
    root = tree.getroot()
    featureList = root.findall('karaf:feature', ns)
    for feature in featureList:
        bundlesList = feature.findall('karaf:bundle', ns)
        for child in bundlesList:        
            content = child.text
            idx = content[::-1].find('/')
            fileName = content[len(content) - idx:]        
            featureComponentList.append(fileName + ".jar")        
    return featureComponentList

def identifyHsipDeploySource(modulePath):
    hsipHome = None
    targetFolder = os.path.join(modulePath, 'target')
    for root, subFolders, files in os.walk(targetFolder):
        for folder in subFolders:
            if os.path.exists(os.path.join(root, folder, 'deploy')):                
                for fileName in os.listdir(os.path.join(root, folder, 'deploy')):
                    if fileName.endswith('.xml'):
                        hsipHome = os.path.join(root, folder)
                        break
        if not hsipHome == None: break
    return hsipHome

def startTomcatScript(config):
    scripts = []
    tomcatHome = getEnvVariableValueFromConfig("catalina_home", config)
    scripts.append("del /f /s /q " + os.path.join(tomcatHome, "logs", "*"))
    scripts.append("rmdir /s /q " + os.path.join(tomcatHome, "work", "Catalina"))
    scripts.append("cd /d " + os.path.join(tomcatHome, "bin"))
    scripts.append("start catalina.bat run")
    return scripts

def startServiceMixScript(config):
    scripts = []
    servicemixHome = getEnvVariableValueFromConfig("servicemix_home", config)
    scripts.append("del /f /s /q " + os.path.join(servicemixHome, "data", "log", "*"))
    scripts.append("del /f /s /q " + os.path.join(servicemixHome, "Carefx", "Common", "logs", "*"))
    scripts.append("cd /d " + os.path.join(servicemixHome, "bin"))
    scripts.append("start servicemix")
    return scripts

def cleanServiceMixCacheScript(config):
    scripts = []
    servicemixHome = getEnvVariableValueFromConfig("servicemix_home", config)
    for bundle in os.listdir(os.path.join(servicemixHome, "data", "cache")):
        scripts.append("rmdir /s /q " + os.path.join(servicemixHome, "data", "cache", bundle))
    return scripts