from mss import mss
from PIL import Image
from datetime import datetime
import os, errno
from getsqldata import *


uid = getCurrentUser()
email = getRowValue('Users',uid)[1]
dir_path = getRowValue('Setting',uid)
path = os.path.join(dir_path[3],'Screenshot')

qual = getRowValue('Screenshot',uid)[8]
#print(qual)

try:
    os.makedirs(path)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

with mss() as sct:
    pathName = path +'\\'+ datetime.now().strftime('%Y_%m_%d-%H_%M_%S-')+email+ '.jpeg'
    print(pathName)
    for filename in sct.save():
        sct.shot()
        # print(filename)
        filename = sct.shot(mon=-1, output=pathName)

        image = Image.open(pathName)
        image.save(pathName, format="JPEG" ,quality=qual, optimize=True)
        print("Screenshot sucessful!")
