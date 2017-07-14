import os
import json
import datetime as dt
import nhutils as nhu


with open('pap.json', 'r') as config:
    DATA = json.load(config)


listRecentlyModifiedModules, listOfGwtModules = nhu.listRecentlyModifiedModules(DATA['project_home'], DATA['file_types'], DATA["last_run"])

#list all maven projects which were modified
#nhu.MODIFIED_PROJECTS
print  '=========================MODIFIED MAVEN PROJECTS=============================='
for file_path in listRecentlyModifiedModules:
    print file_path
print  '=========================GWT MAVEN PROJECTS=============================='
for file_path in listOfGwtModules:
    print file_path

DATA['last_run'] = str(dt.datetime.now())
with open('pap.json', 'w') as config:
    json.dump(DATA, config, indent=4)