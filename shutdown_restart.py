import subprocess

def shutdown(self):
    subprocess.call(["shutdown", "/l "])

def restart(sef):
    subprocess.call(["shutdown", "/r"])

#timeout la string
def shutdown(sef, timeout):
    subprocess.call(["shutdown", "/r", "/s", timeout])