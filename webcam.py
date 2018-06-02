import cv2 #opencv
import numpy as np
import time
import os, errno
from datetime import datetime

#Tao thu muc Webcam
try:
    os.makedirs("Webcam")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
    
#Lấy danh sách webcam bên c#
cap = cv2.VideoCapture(0)

# while(True):
time.sleep(3)
ret, frame = cap.read()
# cv2.imshow('frame', frame)
pathName = "Webcam\\Shot"+ datetime.now().strftime('-%Y_%m_%d-%H_%M_%S')+ ".jpeg"
cv2.imwrite(pathName, frame)
cv2.destroyAllWindows()

    # cv2.imshow('frame', frame)

    # if cv2.waitKey(1) & 0xFF == ord('q'):  # save on pressing 'y'
        
    #     break

cap.release()
cv2.destroyAllWindows()
