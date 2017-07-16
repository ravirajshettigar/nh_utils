import os
import sys
import subprocess
import datetime as dt

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
            newFile.write(line + '\n')
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
    listJarFiles = []
    for folderPath in moduleFolderList:
        targetFolder = folderPath + os.sep + "target"
        if os.path.exists(targetFolder):
            fileList = os.listdir(targetFolder)
            for fileName in fileList:
                if fileName.endswith(".jar"):
                    listJarFiles.append(targetFolder + os.sep + fileName)
    return listJarFiles

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

def listRecentlyModifiedModules(config):
    listOfModules = []
    listOfGwtModules = []

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
                    for s_root, s_subFolders, s_files in os.walk(folder_path):
                        
                        for exFolder in EXCLUDE_FOLDERS:
                            if exFolder in s_subFolders:
                                s_subFolders.remove(exFolder)

                        for s_folder in s_subFolders:                        
                            if not folder_path in listOfGwtModules:
                                for s_file in s_files:
                                    if s_file.endswith(".gwt.xml"):
                                        listOfGwtModules.append(folder_path)
                                        break
                            if not folder_path in listOfModules:     
                                for s_file in s_files:
                                    file_path = s_root + os.sep + s_file
                                    file_stat = os.stat(file_path)
                                    mtime = dt.datetime.fromtimestamp(file_stat.st_mtime)  
                                    ctime = dt.datetime.fromtimestamp(file_stat.st_ctime)                            
                                    if last_run < mtime or last_run < ctime:
                                        listOfModules.append(folder_path)
                                        break
                            continue               
    return listOfModules, listOfGwtModules

def getEnvironmentVariableScript(config): 
    scriptSteps = []
    if "extended_path_variable" in config.keys():        
        if len(config["extended_path_variable"].strip()) > 0:
            scriptSteps.append("set \"path=" + os.environ["path"] + ';' + config["extended_path_variable"] + "\"")

    if "environment_variables" in config.keys():
        envSetList = config["environment_variables"]
        for envSet in envSetList:
            scriptSteps.append("set " + envSet)
    
    if "enable_fiddler_config" in config.keys() and "extended_fiddler_config" in config.keys():
        scriptSteps.append("set catalina_opts=%catalina_opts% " + config["extended_fiddler_config"])
        scriptSteps.append("set karaf_opts=%karaf_opts% " + config["extended_fiddler_config"])
    
    if "enable_debug_config" in config.keys():
        if "extended_catalina_debug_config" in config.keys():
            scriptSteps.append("set catalina_opts=%catalina_opts% " + config["extended_catalina_debug_config"])
        if "extended_karaf_debug_config" in config.keys():
            scriptSteps.append("set karaf_opts=%karaf_opts% " + config["extended_karaf_debug_config"])
    
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