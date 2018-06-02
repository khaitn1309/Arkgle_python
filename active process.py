import wmi
import psutil

#process.ProcessId, process.Name

c = wmi.WMI()

for process in c.Win32_Process():
    print(process.ProcessId, process.Name, process.ExecutablePath)

process = psutil.Process(1460)
process.terminate()
