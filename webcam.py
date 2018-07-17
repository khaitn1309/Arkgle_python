import cv2 #opencv
#import numpy as np
import time
import os, errno
from datetime import datetime
from getsqldata import *

uid = getCurrentUser()
dir_path = getRowValue('Setting',uid)
email = getRowValue('Users',uid)[1]

path = os.path.join(dir_path[2],'Webcam')
#Tao thu muc Webcam
try:
    os.makedirs(path)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
try:    
    #Lấy danh sách webcam
    cap = cv2.VideoCapture(0)

    # while(True):
    time.sleep(3)
    ret, frame = cap.read()
    # cv2.imshow('frame', frame)
    pathName = path +"\\"+ datetime.now().strftime('%Y_%m_%d-%H_%M_%S-')+email+ ".jpeg"
    cv2.imwrite(pathName, frame)
    cv2.destroyAllWindows()

    cap.release()
    cv2.destroyAllWindows()

    print("Successful")
except Exception as e:
    print("Error : " + str(e))
