import os
import sys
import socket
import codecs
import getpass

def saveCredentials(config):
    credentials = []
    hostname = socket.gethostname()
    if "cache_storage" in config.keys():
        secretFile = config["cache_storage"] + os.sep + "user"       
    try:
        with open(secretFile, 'w') as secret:
            username= getpass.getpass("Enter Username: ")
            username = codecs.encode(username + hostname, "rot13")
            password = getpass.getpass("Enter Password: ")
            password = codecs.encode(password + hostname, "rot13")
            secret.write(username + '\n')
            secret.write(password)
            credentials.append(username)
            credentials.append(password)
    except IOError: 
        print("configured 'cache_storage' location either doesn't exist or doesn't have sufficient privileges")
        sys.exit()
        
    return credentials

def readCredentials(config):
    credentials = []
    hostname = socket.gethostname()
    if "cache_storage" in config:
        secretFile = config["cache_storage"] + os.sep + "user"
    try:
        with open(secretFile, 'r') as secret:
            username = secret.readline()
            username = codecs.decode(username, "rot13").replace(hostname, "").strip()
            password = secret.readline()
            password = codecs.decode(password, "rot13").replace(hostname, "")
            credentials.append(username)
            credentials.append(password)
    except IOError: #python 3.0 - FileNotFoundError while python 2.0 doesnt support the same
        credentials = saveCredentials(config)
    return credentials

def processAuthenticationInfo(config):
    credentials = readCredentials(config)
    if len(credentials) == 2:
        print("Loaded Authentication Info Successfully")
    else:
        print("There was some problem while loading Authentication Info, System will exit")
        sys.exit()
    return credentials