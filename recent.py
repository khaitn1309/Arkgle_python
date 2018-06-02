import os

path = os.path.expanduser('~') + r"\AppData"
files = os.listdir(path + r"\Roaming\Microsoft\Windows\Recent")
for item in files:
    if item.endswith('.lnk'):
        print (item)