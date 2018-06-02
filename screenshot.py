from mss import mss
from PIL import Image
from datetime import datetime
import os, errno

try:
    os.makedirs("Screenshot")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
    
with mss() as sct:
    pathName = "Screenshot\\Screen"+ datetime.now().strftime('-%Y_%m_%d-%H_%M_%S')+ ".jpeg"
    # for filename in sct.save():
        # sct.shot()
        # print(filename)
    filename = sct.shot(mon=-1, output=pathName)

image = Image.open(pathName)
image.save(pathName, format="JPEG", quality=100, optimize=True)
