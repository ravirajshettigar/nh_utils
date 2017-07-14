import os
import datetime as dt

def listRecentlyModifiedModules(ROOT_DIR, FILE_TYPES, LAST_RUN):
    listOfModules = []
    listOfGwtModules = []
    if bool(LAST_RUN.strip()):
        last_run = dt.datetime.strptime(LAST_RUN, '%Y-%m-%d %H:%M:%S.%f')
    else:
        last_run = dt.datetime.now() - dt.timedelta(days=365)
    
    exFolderList = ['.svn', '.settings', 'target']
    for root, subFolders, files in os.walk(ROOT_DIR):
        
        for exFolder in exFolderList:
            if exFolder in subFolders:
                subFolders.remove(exFolder)

        for folder in subFolders:               
            folder_path = root + os.sep + folder            
            is_gwt_project =False
            pom_xml = folder_path + os.sep + 'pom.xml'
            src_folder = folder_path + os.sep + 'src' + os.sep + 'main'
            if os.path.exists(pom_xml) and os.path.exists(src_folder):
                for s_root, s_subFolders, s_files in os.walk(folder_path):
                    
                    for exFolder in exFolderList:
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

def generatePaPBatchScript():
    scriptSteps = []

    scriptSteps + setEnvironmentVariables(config)    

    return scriptSteps

def setEnvironmentVariables(config) 
    scriptSteps = []
    
    scriptSteps.append("set " + os.environment["path"] + ';' + config["path"])
    scriptSteps.append("set " + config["java_home"])
    scriptSteps.append("set " + config["catalina_home"])
    scriptSteps.append("set " + config["catalina_opts"])
    scriptSteps.append("set " + config["carefx_home"])
    scriptSteps.append("set " + config["servicemix_home"])
    scriptSteps.append("set " + config["karaf_opts"])
    scriptSteps.append("set " + config["maven_home"])
    scriptSteps.append("set " + config["maven_opts"] ) 
    
    return scriptSteps