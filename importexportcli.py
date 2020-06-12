"""Export bot CLI
Usage:
    importexportcli.py
    importexportcli.py -u <username>
    importexportcli.py -s <util> -u <username> -k <apikey> -url <url> -id <botid> -pkg <packages> -l <location>
    importexportcli.py -s <util> -u <username> -k <apikey> -url <url> -l <location>
    importexportcli.py -h|--help
    importexportcli.py -v|--version
Options:
    <util> Mandatory argument for either to do import or export. Export works right now as of 1.0. Example: 'export'
    <username>  Mandatory argument for Control Room username. 
    <apikey>  Mandatory argument for apikey for the username. If you have a quotation mark, put an extra quotation mark right after it to escape it. 
    <url>  Mandatory argument for Control Room URL. Example: 'http://CRurl.com/'
    <botid>  Mandatory argument for fileID of the check-in bot. 
    <packages>  Mandatory argument to include packages with the export. Example: true or false
    <location>  Mandatory argument for where to import or export the bot. Needs to include the full path of the zip file. Example: C:/ExportDirectory/test1.zip
    -h --help  Show this screen.
    -v --version  Show version.
"""

import requests
import time
import json
import os
import zipfile
import string
import random
from docopt import docopt

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def CRauth(url, user, apikey):
    authurl = url+"v1/authentication"
    data = {"Username": user,"apiKey": apikey}
    data_json = json.dumps(data)
    headers = {'Content-Type':'application/json'}
    response = requests.post(authurl, data=data_json, headers=headers)
    output = response.json()
    token = output['token']
    return token

def exportbot(url, user, apikey, botid, packages, location):
    token = CRauth(url, user, apikey)
    crqurl = url+"v2/blm/export"
    botname = randomString(8)
    data = {"name":botname, "fileIds":[botid], "includePackages":packages}
    data_json = json.dumps(data)
    headers = {'Content-Type':'application/json',"X-Authorization":token}
    response = requests.post(crqurl, data=data_json, headers=headers)
    output = response.json()
    requestID = output['requestId']
    status = exportstatus(url, token, requestID)
    cnt = 0
    while (status != 'COMPLETED'):
        print("waiting")
        time.sleep(5)
        status = exportstatus(url, token, requestID)
        cnt = cnt+1
        if cnt > 10:
            print("export failed")
            break
    if status == 'COMPLETED':
        downloadfile(url, token, requestID, location)
    return "bot exported"

def exportstatus(url, token, reqid):
    crqurl = url+"v2/blm/status/"+reqid
    headers = {'Accept':'application/json',"X-Authorization":token}
    response = requests.get(crqurl, headers=headers)
    output = response.json()
    status = output['status']
    exportstatus.downloadId = output['downloadFileId']
    return status

def downloadfile(url, token, reqid, location):
    exportstatus(url, token, reqid)
    downloadid = exportstatus.downloadId
    crqurl = url+"v2/blm/download/"+downloadid
    headers = {'Accept':'application/json',"X-Authorization":token}
    response = requests.get(crqurl, headers=headers)
    with open(location, mode='wb') as localfile:
        localfile.write(response.content)

def importbot(url, user, apikey, location):
    token = CRauth(url, user, apikey)
    crqurl = url+"v2/blm/import"
    payload = {'publicWorkspace': 'true','actionIfExisting': 'OVERWRITE'}
    files = [('upload', open(location,'rb'))]
    headers = {'X-Authorization': token}
    response = requests.post(crqurl, headers=headers, data = payload, files = files)
    output = response.json()
    return "Import Request Submitted"


#print(exportbot(CRurl, Username, apiKey1, botname1, botid1, "false"))

#print(exportstatus(CRurl, token1, reqid1))

#downloadfile(CRurl, token1, reqid1, location1)

#exportbot(CRurl, Username, apiKey1, botid1, "true", location1)

arguments = docopt(__doc__, version='2.0')
if arguments['<util>'] == 'Export':
    print(exportbot(arguments['<url>'], arguments['<username>'], arguments['<apikey>'], arguments['<botid>'], arguments['<packages>'], arguments['<location>']))
    #print(arguments['<url>'], arguments['<username>'], arguments['<apikey>'], arguments['<botid>'], arguments['<packages>'], arguments['<location>'])
elif arguments['<util>'] == 'Import':
    print(importbot(arguments['<url>'], arguments['<username>'], arguments['<apikey>'], arguments['<location>']))
elif arguments['<username>']:
    print(arguments['<username>'])
else:
    print("did not execute")