"""Export bot CLI
Usage:
    importexportcli.py
    importexportcli.py -u <username>
    importexportcli.py -s <util> -u <username> -k <apikey> -url <url> -id <botid> -pkg <packages> -l <location>
    importexportcli.py -h|--help
    importexportcli.py -v|--version
Options:
    <util> Mandatory argument for either to do import or export. Export works right now as of 1.0. Example: 'export'
    <username>  Mandatory argument for Control Room username. 
    <apikey>  Mandatory argument for apikey for the username. If you have a quotation mark, put an extra quotation mark right after it to escape it. 
    <url>  Mandatory argument for Control Room URL. Example: 'http://CRurl.com/'
    <botid>  Mandatory argument for fileID of the check-in bot. 
    <packages>  Mandatory argument to include packages with the export. Example: true or false
    <location>  Mandatory argument for where to export the bot. Needs to include the full path of the zip file. Example: C:/ExportDirectory/test1.zip
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

# Test Parameters
'''
CRurl = 'http://linuxa2019/'
Username = 'apiuser'
apiKey1 = '" ;e7ew(FSZM$<FQ]w4(n~ajnkX5&A22Pp\+|1OP'
botname1 = "Exportbottst123"
botid1 = '996'
token1 = 'eyJhbGciOiJSUzUxMiJ9.eyJzdWIiOiI2IiwiY2xpZW50VHlwZSI6IldFQiIsImxpY2Vuc2VzIjpbIkFOQUxZVElDU0NMSUVOVCJdLCJhbmFseXRpY3NMaWNlbnNlc1B1cmNoYXNlZCI6eyJBbmFseXRpY3NDbGllbnQiOnRydWUsIkFuYWx5dGljc0FQSSI6dHJ1ZX0sInRlbmFudFV1aWQiOiIwMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDAiLCJoeWJyaWRUZW5hbnQiOiIiLCJpYXQiOjE1OTE5MDQwMTcsImV4cCI6MTU5MTkwNTIxNywiaXNzIjoiQXV0b21hdGlvbkFueXdoZXJlIiwibmFub1RpbWUiOjM3NTk2OTMwODU1NzQ4MDB9.WfPiiUEfRoo3GMnpj_YRMPG0lec95teQof3qFSBznzT4YVC6U9PpGyjoc_JQUSPEJTjd61T5EQYs2ZxtZWZQ2n8Z-cLuuCQ0Aj4Bu_0DgD2tZum5xS678VjHrwL4s38e0NyvFiXEEoMoI71W2g6tP4TNZfzRcRNLpzr_KjjjAZU-iQtbT9VyNZsea3irahkSGWxX9xfd0REnaA9sr7z9qynj35Yjc8KpbQHTvXGRjWhhkVYrxbVB2H9oNHs7Bj1Rs7i-N9tc1gHk7WE7oRriHpj-zt6pJKwaxjUprKqfwgJ7-WhFBVMZ9uKXH0ONl5wGQKq4syBX-jpPf29sJfliLg'
reqid1 = 'f79a8ac9-9905-4ed0-ba5e-b8a8ee18bcfb'
location1 = 'C:/Users/shoaibali/OneDrive - Automation Anywhere/Testing/CICDtesting/test1.zip'
'''

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


#print(exportbot(CRurl, Username, apiKey1, botname1, botid1, "false"))

#print(exportstatus(CRurl, token1, reqid1))

#downloadfile(CRurl, token1, reqid1, location1)

#exportbot(CRurl, Username, apiKey1, botid1, "true", location1)

arguments = docopt(__doc__, version='DEMO 1.0')
if arguments['<util>'] == 'Export':
    print(exportbot(arguments['<url>'], arguments['<username>'], arguments['<apikey>'], arguments['<botid>'], arguments['<packages>'], arguments['<location>']))
    #print(arguments['<url>'], arguments['<username>'], arguments['<apikey>'], arguments['<botid>'], arguments['<packages>'], arguments['<location>'])
elif arguments['<username>']:
    print(arguments['<username>'])
else:
    print("did not execute")