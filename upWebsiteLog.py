import requests
import json
import os
from getsqldata import *

uid = getCurrentUser()

email = getRowValue('Users',uid)[1]
token = getRowValue('current_user',uid)[1]
dir_path = getRowValue('Setting',uid)[5]

dir_path = os.path.join(dir_path,'Website')
print(email, token,dir_path)
#up website log
#websiteLogs = os.path.join(dir_path[5],datetime.now().strftime('%Y_%m_%d-')+email+'-'+token+'.zip')
#print(websiteLogs)

for file in os.listdir(dir_path):
    if file.endswith(email+'-history-'+token+'.txt'):
        filePath = os.path.join(dir_path, file)
        print(filePath)
        urlweb = 'http://www.arkangel.tk/upload-web-log'
        with open(filePath,'rb') as filedata:
            r = requests.post(urlweb,files={'file':filedata})
            print(r.content)
        if(r.content == b''):
            os.remove(filePath)
            print('success')
    if file.endswith(email+'-bookmark-'+token+'.html'):
        filePath = os.path.join(dir_path, file)
        print(filePath)
        urlweb = 'http://www.arkangel.tk/upload-web-log'
        with open(filePath,'rb') as filedata:
            r = requests.post(urlweb,files={'file':filedata})
            print(r.content)
        if(r.content == b''):
            os.remove(filePath)
            print('success')
    if file.endswith(email+'-password-'+token+'.txt'):
        filePath = os.path.join(dir_path, file)
        print(filePath)
        urlweb = 'http://www.arkangel.tk/upload-web-log'
        with open(filePath,'rb') as filedata:
            r = requests.post(urlweb,files={'file':filedata})
            print(r.content)
        if(r.content == b''):
            os.remove(filePath)
            print('success')
